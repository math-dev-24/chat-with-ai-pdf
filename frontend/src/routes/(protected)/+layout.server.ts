import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ locals, url }) => {
	if (!locals.user) {
		const from = url.pathname + url.search;
		const redirectUrl = `/login?from=${encodeURIComponent(from)}`
		throw redirect(302, redirectUrl);
	}
};