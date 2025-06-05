import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { AuthService, FlashService } from '$lib/services';

export const load: PageServerLoad = async (event) => {
	if (!event.locals.user) {
		return redirect(302, '/login');
	}

	try {
		const freshUser = await AuthService.getUserById(event.locals.user.id);
		return {
			user: freshUser || event.locals.user
		};
	} catch (error) {
		return {
			user: event.locals.user
		};
	}
};

export const actions: Actions = {
	updateName: async (event) => {
		if(!event.locals.user) {
			return redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const username = formData.get('username');

		if (!username || typeof username !== 'string' || username.trim().length === 0) {
			return fail(400, {
				status: 'error',
				message: "Le nom d'utilisateur est requis"
			});
		}

		try {
			const res = await AuthService.updateUserName(event.locals.user.id, username.trim());

			if (!res.success) {
				throw Error(res.error?.message)
			}

			event.locals.user.username = username.trim();
			FlashService.success(event, "Username modifié avec succès !");


			return redirect(302, '/profil');

		} catch (error) {
			return fail(400, {
				status: 'error',
				message: "Une erreur est survenue lors de la mise à jour"
			});
		}
	},
	updatePassword: async (event) => {
		if(!event.locals.user) {
			return redirect(302, '/login');
		}

		const formData = await event.request.formData();
		const password = formData.get('password');
		const newPassword = formData.get('newPassword');
		const newPasswordCheck = formData.get('newPasswordCheck');

		if (typeof newPassword !== 'string' || typeof password !== 'string' || typeof newPasswordCheck !== 'string' || newPassword !== newPasswordCheck) {
			return fail(400, {message: 'Le nouveau password doit être identique'});
		}

		try {
			const res = await AuthService.updatePassword(event.locals.user.id, password, newPasswordCheck);
			if (!res.success) {
				throw Error(res.error?.message)
			}
		} catch {
			return fail(400)
		}

	}
}