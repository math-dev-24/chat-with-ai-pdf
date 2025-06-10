import { fail, redirect } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import type { Actions, PageServerLoad } from './$types';
import { AuthService } from "$lib/services/auth.service";
import {FlashService} from "$lib/services";


function isValidRedirectUrl(url: string): boolean {
	return url.startsWith('/') && !url.startsWith('//');
}

export const load: PageServerLoad = async ({locals, url}) => {
	if (locals.user) {
		const from = url.searchParams.get('from');
		const redirectTo = (from && isValidRedirectUrl(from)) ? from : '/';
		throw redirect(302, redirectTo);
	}
	return {
		from: url.searchParams.get('from') || '/'
	};
};

export const actions: Actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const username = formData.get('username');
		const password = formData.get('password');
		const from = formData.get('from')?.toString() || '/'; // ← Récupérer le paramètre 'from'

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

		const redirectTo = isValidRedirectUrl(from) ? from : '/';
		return redirect(302, redirectTo);
	}
};