export type ChatMessage = {
	id: string;
	role: 'system' | 'user' | 'assistant',
	message: string;
}

export type StateChat = {
	answer: string;
	inLoading: boolean;
	context: string[],
	dialog: ChatMessage[],
	errors: string[],
	showContext: boolean
}