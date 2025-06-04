export interface AuthResult<T> {
	success: boolean;
	data?: T;
	error?: {
		code: 'VALIDATION_ERROR' | 'AUTH_ERROR' | 'SERVER_ERROR';
		message: string;
	};
}