import type { PageServerLoad } from './$types';
import { ApiService, ConversationService, FlashService } from '$lib/services';
import { type Actions, fail, redirect } from '@sveltejs/kit';
import type { ConversationWithMessages } from '$lib/types';
import type { Conversation } from '$lib/server/db/schema';


export const load: PageServerLoad = async (event) => {
	if (!event.locals.user) {
		return redirect(302, '/login');
	}
	const { params } = event;

	if (!params.id) {
		return redirect(302, '/chat/new');
	}

	if (params.id === 'new') {
		return {
			isNew: true,
			list_conversations: await ConversationService.getUserConversation(event.locals.user.id)
		};
	}

	try {
		const conversation: ConversationWithMessages = await ConversationService.getConversation(
			params.id
		);

		const listConversation: Conversation[] = await ConversationService.getUserConversation(
			event.locals.user.id
		);

		return {
			actual_conversation: conversation,
			list_conversations: listConversation,
			isNew: false
		};
	} catch (error) {
		console.error('Error loading conversation:', error);
		FlashService.error(event, 'Conversation non trouvée');
		return redirect(302, '/chat/new');
	}
};

export const actions: Actions = {
	updateNameConversation: async (event) => {
		if (!event.locals.user) {
			throw redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const id = formData.get('id');
		const name = formData.get('name');

		if (!id || !name || typeof id !== 'string' || typeof name !== 'string') {
			FlashService.error(event, 'Id ou name vide !');
			return fail(400);
		}

		await ConversationService.updateNameConversation(event.locals.user.id, id, name);
		FlashService.success(event, "Conversation mise à jour !");
		throw redirect(302, `/chat/${id}`);
	},

	deleteConversation: async (event) => {
		if (!event.locals.user) {
			throw redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const fromId = formData.get('from')?.toString();
		const convId = event.params.id;

		if (!convId) {
			FlashService.error(event, "Pas d'id !");
			return fail(400, {error: "Pas d'id !"});
		}

		try {
			await ConversationService.deleteConversation(event.locals.user.id, convId);
			FlashService.success(event, 'Conversation supprimée !');

			if (fromId && fromId !== convId) {
				return { success: true };
			}

			const list = await ConversationService.getUserConversation(event.locals.user.id);
			if (list.length > 0) {
				throw redirect(302, `/chat/${list[0].id}`);
			}
			throw redirect(302, '/chat/new');
		} catch (error) {
			console.error('Error deleting conversation:', error);
			FlashService.error(event, 'Erreur lors de la suppression de la conversation');
			return fail(500, {error: "Erreur lors de la suppression de la conversation"});
		}
	},

	postMessage: async (event) => {
		if (!event.locals.user) {
			throw redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const convId = event.params.id;
		const answer = formData.get('answer');

		if (!convId || !answer || typeof answer !== 'string') {
			FlashService.error(event, 'Une erreur est survenue !');
			return fail(400, {error: "Une erreur est survenue !"});
		}

		try {
			const res = await ApiService.ask(event.locals.user.id, answer, [])
			if(!res.success) {
				FlashService.error(event, res.error);
				return fail(400, {error: res.error});
			}
			
			const data = res.data

			await ConversationService.addMessage(event.locals.user.id, convId, answer);
			await ConversationService.addMessage(event.locals.user.id, convId, data.response, 'assistant')
			
			if (data.context) {
				await ConversationService.addContext(convId, data.context, data.sources);
			}

			return redirect(302, `/chat/${convId}`);
		} catch (e) {
			console.error('Error posting message:', e);
			FlashService.error(event, 'Une erreur est survenue lors de l\'envoi du message');
				return fail(500, { error: e instanceof Error ? e.message : 'Une erreur inconnue est survenue' });
		}
	},

	createNewConversation: async (event) => {
		if (!event.locals.user) {
			return redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const name = formData.get('name')?.toString() || 'Nouvelle conversation';

		try {
			const { id } = await ConversationService.initConversation(name, event.locals.user.id);
			FlashService.success(event, 'Nouvelle conversation créée !');
			return redirect(302, `/chat/${id}`);
		} catch (error) {
			FlashService.error(event, 'Erreur lors de la création de la conversation');
			return fail(500, {error: "Erreur lors de la création de la conversation"});
		}
	}
};
