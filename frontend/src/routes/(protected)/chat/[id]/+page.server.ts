import type { PageServerLoad } from './$types';
import { ApiService, ConversationService, FlashService } from '$lib/services';
import { type Actions, fail, redirect } from '@sveltejs/kit';
import type { ConversationWithMessages } from '$lib/types';
import type { Conversation } from '$lib/server/db/schema';


export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user) {
		throw redirect(302, '/login');
	}

	if (!params.id || params.id === 'new') {
		const { id } = await ConversationService.initConversation('default', locals.user.id);
		throw redirect(302, `/chat/${id}`);
	}

	try {
		const conversation: ConversationWithMessages = await ConversationService.getConversation(
			params.id
		);
		const listConversation: Conversation[] = await ConversationService.getUserConversation(
			locals.user.id
		);

		return {
			actual_conversation: conversation,
			list_conversations: listConversation
		};
	} catch {
		redirect(302, '/chat/new');
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
		redirect(302, `/chat/${id}`);
	},

	deleteConversation: async (event) => {
		if (!event.locals.user) {
			throw redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const fromId = formData.get('from');
		const convId = event.params.id;

		if (!convId) {
			FlashService.error(event, "Pas d'id !");
		}

		await ConversationService.deleteConversation(event.locals.user.id, convId as string);

		FlashService.success(event, 'Converssation supprimé !');

		if (fromId != convId) {
			return {
				success: true
			}
		}

		const list = await ConversationService.getUserConversation(event.locals.user.id);

		if (list.length > 0) {
			return redirect(302, `/chat/${list[0].id}`);
		}
		return redirect(302, '/chat/new');
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
			return fail(400);
		}

		try {
			const res = await ApiService.ask(answer, [])

			const data = await res.json()

			await ConversationService.addMessage(event.locals.user.id, convId, answer);
			await ConversationService.addMessage(event.locals.user.id, convId, data.response, 'assistant')
			
			if (data.context) {
				await ConversationService.addContext(convId, data.context);
			}

			redirect(302, `/chat/${convId}`);
		} catch (e) {
			fail(400, {error: e})
		}
	}
};
