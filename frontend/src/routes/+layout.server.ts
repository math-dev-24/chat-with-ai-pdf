import type { LayoutServerLoad } from './$types';
import {FlashService} from "$lib/services";

export const load: LayoutServerLoad = async ({ locals, cookies }) => {
	return {
		user: locals.user ?? null,
		session: locals.session ?? null,
		flashMessage: FlashService.read(cookies)
	};
};