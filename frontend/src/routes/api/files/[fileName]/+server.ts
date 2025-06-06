import { json } from '@sveltejs/kit';
import { base_url_api } from '$lib/const';

export const DELETE = async ({ params } : {params: {fileName: string}}) => {
	try {
		const response = await fetch(`${base_url_api}/files/${params.fileName}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			throw new Error(`Erreur HTTP: ${response.status}`);
		}

		return json({ success: true });
	} catch (error) {
		console.error('Erreur lors de la suppression du fichier:', error);
		return json(
			{ 
				success: false, 
				error: error instanceof Error ? error.message : 'Une erreur est survenue' 
			},
			{ status: 500 }
		);
	}
}; 