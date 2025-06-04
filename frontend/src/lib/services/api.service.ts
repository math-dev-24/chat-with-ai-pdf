import { base_url_api } from '$lib/const';


export class ApiService {
	static async getStat() {
		return await fetch(`${base_url_api}/stat`)
	}

	static async loadPdf() {
		return await fetch(`${base_url_api}/pdfs/process-all`, {
			method: 'POST'
		});
	}

	static async ask(answer: string, historics: any[]) {
		return await fetch(`${base_url_api}/ask`, {
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
	}
}