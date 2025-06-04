import type { PageServerLoad } from './$types';
import { base_url_api } from '$lib/const';
import { type Actions, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async (event) => {
	try {

		const statResponse = await fetch(`${base_url_api}/stat`)

		if (!statResponse.ok) {
			throw new Error('Failed to fetch data');
		}

		return {
			stat: await statResponse.json()
		};
	} catch (error) {
		console.error('Load error:', error);
		return {
			stat: null,
			files: []
		};
	}
};