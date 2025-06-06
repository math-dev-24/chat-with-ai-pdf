import type { RequestEvent } from '@sveltejs/kit';
import type { Cookies } from '@sveltejs/kit';

export type FlashMessage = {
	type: 'success' | 'error' | 'warning' | 'info';
	message: string;
}

export class FlashService {
	private static readonly COOKIE_NAME = 'flash-message';
	private static readonly COOKIE_MAX_AGE = 60;

	static set(event: RequestEvent, type: FlashMessage['type'], message: string): void {
		const flashMessage: FlashMessage = { type, message };

		event.cookies.set(this.COOKIE_NAME, JSON.stringify(flashMessage), {
			path: '/',
			maxAge: this.COOKIE_MAX_AGE,
			httpOnly: false,
			secure: process.env.NODE_ENV === 'production',
			sameSite: 'lax'
		});
	}

	static read(cookies: Cookies): FlashMessage | null {
		const flashCookie = cookies.get(this.COOKIE_NAME);

		if (!flashCookie) return null;

		try {
			const flashMessage = JSON.parse(flashCookie);

			cookies.delete(this.COOKIE_NAME, { path: '/' });

			return flashMessage;
		} catch (error) {
			console.error('Erreur lors de la lecture du message flash:', error);
			cookies.delete(this.COOKIE_NAME, { path: '/' });
			return null;
		}
	}

	static success(event: RequestEvent, message: string): void {
		this.set(event, 'success', message);
	}

	static error(event: RequestEvent, message: string): void {
		this.set(event, 'error', message);
	}

	static warning(event: RequestEvent, message: string): void {
		this.set(event, 'warning', message);
	}

	static info(event: RequestEvent, message: string): void {
		this.set(event, 'info', message);
	}
	
	static crud = {
		created: (event: RequestEvent, entityName: string) =>
			this.success(event, `${entityName} créé avec succès !`),

		updated: (event: RequestEvent, entityName: string) =>
			this.success(event, `${entityName} mis à jour avec succès !`),

		deleted: (event: RequestEvent, entityName: string) =>
			this.success(event, `${entityName} supprimé avec succès !`),

		createError: (event: RequestEvent, entityName: string) =>
			this.error(event, `Erreur lors de la création de ${entityName}`),

		updateError: (event: RequestEvent, entityName: string) =>
			this.error(event, `Erreur lors de la mise à jour de ${entityName}`),

		deleteError: (event: RequestEvent, entityName: string) =>
			this.error(event, `Erreur lors de la suppression de ${entityName}`),

		notFound: (event: RequestEvent, entityName: string) =>
			this.error(event, `${entityName} introuvable`),

		validationError: (event: RequestEvent) =>
			this.error(event, 'Veuillez vérifier les données saisies'),

		unauthorized: (event: RequestEvent) =>
			this.error(event, 'Vous n\'êtes pas autorisé à effectuer cette action'),

		serverError: (event: RequestEvent) =>
			this.error(event, 'Une erreur interne s\'est produite')
	};
}