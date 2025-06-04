import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { AuthService } from "$lib/services/auth.service";


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

		const registerResult = await AuthService.register(username, password);

		if (!registerResult.success) {
			const statusCode = registerResult.error?.code === 'VALIDATION_ERROR' ? 400 : 500;
			return fail(statusCode, {
				message: registerResult.error?.message || 'Registration failed',
				type: 'error'
			});
		}
		return redirect(302, '/login');
	}
};