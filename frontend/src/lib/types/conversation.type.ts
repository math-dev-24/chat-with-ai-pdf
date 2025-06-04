import type { Conversation, Message } from '$lib/server/db/schema';


export interface ConversationWithMessages extends Conversation {
	messages: Message[];
}