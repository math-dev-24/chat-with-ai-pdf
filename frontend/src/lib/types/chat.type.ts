export type ChatMessage = {
	id: string;
	role: 'system' | 'user' | 'assistant',
	message: string;
}

export type Context = {
	id: string;
	conversationId: string;
	content: string;
	createdAt: string;
	sources: string[];
}

export type StateChat = {
	answer: string;
	inLoading: boolean;
	errors: string[],
	showContext: boolean
}