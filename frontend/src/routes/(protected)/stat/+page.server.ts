import type { PageServerLoad } from './$types';
import { ApiService, FlashService } from '$lib/services';

export const load: PageServerLoad = async (event) => {
	if (!event.locals.user) {
		return {
			stat: null,
			files: []
		};
	}

	try {
		const statResponse = await ApiService.getStat(event.locals.user.id)	

		if (!statResponse.success) {
			throw new Error(statResponse.error)
		}

		return {
			stat: statResponse.data
		};

	} catch (error) {
		console.error('Load error:', error);
		FlashService.error(event, 'Une erreur est survenue lors de la récupération des statistiques')

		return {
			stat: null,
			files: []
		};
	}
};