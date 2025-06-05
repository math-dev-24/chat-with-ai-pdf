export type ChatMessage = {
	id: string;
	role: 'system' | 'user' | 'assistant',
	message: string;
}

export type StateChat = {
	answer: string;
	inLoading: boolean;
	context: string[],
	errors: string[],
	showContext: boolean
}