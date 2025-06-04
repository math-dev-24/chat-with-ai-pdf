import { fail, redirect } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import type { Actions, PageServerLoad } from './$types';
import { AuthService } from "$lib/services/auth.service";
import {FlashService} from "$lib/services";

export const load: PageServerLoad = async (event) => {
	if (event.locals.user) {
		return redirect(302, '/');
	}
	return {};
};

export const actions: Actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const username = formData.get('username');
		const password = formData.get('password');

		if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
			return fail(400, { message: 'Missing username or password', type: 'error' });
		}

		const loginResult = await AuthService.login(username, password);

		if (!loginResult.success) {
			return fail(400, {
				message: loginResult.error?.message || 'Login failed',
				type: 'error'
			});
		}

		const existingUser = loginResult.data!;

		const sessionToken = auth.generateSessionToken();
		const session = await auth.createSession(sessionToken, existingUser.id);
		auth.setSessionTokenCookie(event, sessionToken, session.expiresAt);

		FlashService.success(event, 'Vous êtes maintenant connecté !');

		return redirect(302, '/');
	}
};