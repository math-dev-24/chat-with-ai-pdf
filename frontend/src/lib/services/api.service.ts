import { base_url_api } from '$lib/const';
import type { ServiceResponse } from '$lib/types/service.type';
import type { Stat, AskResponse } from '$lib/types';

export class ApiService {
	static async getStat(userId: string): Promise<ServiceResponse<Stat>> {
		try {
			const response = await fetch(`${base_url_api}/stat?user_id=${userId}`, {
				method: 'GET',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				}
			})
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

	static async loadPdf(userId: string, custom_pdf_path: string|null = null): Promise<ServiceResponse<void>> {
		try {
			const response = await fetch(`${base_url_api}/pdfs/process-all`, {
				method: 'POST',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					user_id: userId,
					...(custom_pdf_path ? { custom_pdf_path } : {})
				})
			});
			if (!response.ok) {
				throw new Error('Une erreur est survenue lors du traitement des pdfs')
			}
			return {
				success: true,
				data: undefined
			}
		} catch (error) {
			console.error('Error loading PDF:', error);
			return {
				success: false,
				error: "Une erreur est survenue lors du traitement des pdfs"
			}
		}
	}

	static async ask(userId: string, question: string, historics: any[]): Promise<ServiceResponse<AskResponse>> {
		try {
			const response = await fetch(`${base_url_api}/ask`, {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				user_id: userId,
				question: question,
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

	static async deleteFile(userId: string, fileName: string): Promise<ServiceResponse<void>> {
		try {
			const response = await fetch(`${base_url_api}/files`, {
				method: 'DELETE',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					user_id: userId,
					file_name: fileName
				})
			});
			if (!response.ok) {
				throw new Error('Une erreur est survenue lors de la suppression du fichier')
			}
			return {
				success: true,
				data: undefined
			}
		} catch {
			return {
				success: false,
				error: "Une erreur est survenue lors de la suppression du fichier"
			}
		}
	}
}