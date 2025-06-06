import { base_url_api } from '$lib/const';
import type { ServiceResponse } from '$lib/types/service.type';
import type { Stat, AskResponse } from '$lib/types';

export class ApiService {
	static async getStat(): Promise<ServiceResponse<Stat>> {
		try {
			const response = await fetch(`${base_url_api}/stat`)
			const data = await response.json()
			return {
				success: true,
				data: data
			}
		} catch {
			return {
				success: false,
				error: "Une erreur est survenue lors de la récupération des statistiques"
			}
		}
	}

	static async loadPdf(): Promise<ServiceResponse<void>> {
		try {
			const response = await fetch(`${base_url_api}/pdfs/process-all`, {
				method: 'POST'
			});
			if (!response.ok) {
				throw new Error('Une erreur est survenue lors du traitement des pdfs')
			}
			return {
				success: true,
				data: undefined
			}
		} catch {
			return {
				success: false,
				error: "Une erreur est survenue lors du traitement des pdfs"
			}
		}
	}

	static async ask(answer: string, historics: any[]): Promise<ServiceResponse<AskResponse>> {
		try {
			const response = await fetch(`${base_url_api}/ask`, {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				question: answer,
				historics: historics
			})
		})
		if (!response.ok) {
			throw new Error('Une erreur est survenue lors de la réponse à la question')
		}
		const data = await response.json()

		return {
			success: true,
			data: data
		}
		} catch {	
			return {
				success: false,
				error: "Une erreur est survenue lors de la réponse à la question"
			}
		}
	}
}