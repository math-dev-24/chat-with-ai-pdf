import type { Conversation, Message, Context } from '$lib/server/db/schema';


export type ConversationWithMessages = Conversation & {
	messages: Message[];
	contexts: Context[];
}

export type AskResponse = {
	question: string;
	response: string;
	context: string;
	context_length: number,
	sources_count: number,
	sources: string[],
	processing_time: null | number,
}