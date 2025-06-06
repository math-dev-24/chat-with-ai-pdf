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

		console.log(username, formData);

		if (!username || typeof username !== 'string' || username.trim().length === 0) {
			return fail(400, {
				status: 'error',
				message: "Le nom d'utilisateur est requis"
			});
		}

		try {
			const res = await AuthService.updateUserName(event.locals.user.id, username.trim());

			if (!res.success) {
				return fail(400, {
					status: 'error',
					message: res.error?.message || "Erreur lors de la mise à jour du nom"
				});
			}

			event.locals.user.username = res.data?.username || username.trim();

			FlashService.success(event, "Nom d'utilisateur modifié avec succès !");

			return {
				success: true,
				status: 'success',
				message: "Mise à jour avec success !"
			};

		} catch (error) {
			console.error('Erreur updateName:', error);
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

		if (typeof newPassword !== 'string' || typeof password !== 'string' || typeof newPasswordCheck !== 'string') {
			return fail(400, {
				status: 'error',
				message: 'Tous les champs sont requis'
			});
		}

		if (password.trim().length === 0 || newPassword.trim().length === 0) {
			return fail(400, {
				status: 'error',
				message: 'Les mots de passe ne peuvent pas être vides'
			});
		}

		if (newPassword !== newPasswordCheck) {
			return fail(400, {
				status: 'error',
				message: 'Les nouveaux mots de passe ne correspondent pas'
			});
		}

		if (newPassword.length < 6) {
			return fail(400, {
				status: 'error',
				message: 'Le nouveau mot de passe doit contenir au moins 6 caractères'
			});
		}

		try {
			const res = await AuthService.updatePassword(event.locals.user.id, password, newPassword);

			if (!res.success) {
				return fail(400, {
					status: 'error',
					message: res.error?.message || "Mot de passe actuel incorrect"
				});
			}

			FlashService.success(event, "Mot de passe modifié avec succès !");

			return {
				success: true,
				status: 'success'
			};

		} catch (error) {
			console.error('Erreur updatePassword:', error);
			return fail(400, {
				status: 'error',
				message: "Une erreur est survenue lors de la mise à jour du mot de passe"
			});
		}
	}
}