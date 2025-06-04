import type { ChatMessage, ConversationWithMessages } from '$lib/types';
import { nanoid } from 'nanoid';
import { db } from '$lib/server/db';
import * as table from "$lib/server/db/schema";
import {eq} from "drizzle-orm";
import { conversation, type Conversation, type Message, message } from '$lib/server/db/schema';



export class ConversationService {

	static async initConversation(name: string, userId: string): Promise<Conversation> {
		const newConversation = {
			id: nanoid(),
			name: name,
			userId: userId,
			createdAt: new Date(),
			updatedAt: new Date(),
		}

		try {
			const tmpConversation = await db.insert(table.conversation).values(newConversation).returning()
			return tmpConversation.at(0) as Conversation;
		} catch {
			throw Error('Error initializing conversation');
		}
	}

	static async getUserConversation(userId: string): Promise<Conversation[]> {
		return db.select().from(table.conversation)
			.where(eq(conversation.userId, userId))
	}

	static async getConversation(id: string): Promise<ConversationWithMessages> {
		const tmpConversation = (await db.select().from(table.conversation)
			.where(eq(conversation.id, id))).at(0);

		if(!tmpConversation){
			throw Error('Error initializing conversation');
		}

		const messages = await db.select().from(table.message)
			.where(eq(message.conversationId, tmpConversation.id))

		return {
			...tmpConversation,
			messages: messages,
		}
	}

	static async updateNameConversation(userId: string, convId: string, name: string): Promise<Conversation> {
		const tmpConversation = (await db.select().from(table.conversation)
			.where(eq(conversation.id, convId))).at(0);

		if(!tmpConversation){
			throw Error('Error initializing conversation');
		}

		if(tmpConversation.userId !== userId){
			throw Error('Error initializing conversation');
		}

		if(tmpConversation.name == name){
			return tmpConversation
		}

		const updated = (await db.update(table.conversation).set({name})
			.where(eq(conversation.id, convId)).returning()).at(0);

		if(!updated){
			throw Error('Error initializing conversation');
		}

		return updated;
	}

	static async addMessage(userId: string, convId: string, answer: string, role: string = 'user'): Promise<Message> {
		const tmpConversation = (await db.select().from(table.conversation)
			.where(eq(conversation.id, convId))).at(0)

		if(!tmpConversation){
			throw Error('Error initializing conversation');
		}

		if (tmpConversation.userId !== userId){
			throw Error('Error initializing conversation');
		}

		const newMessage: Message = {
			id: nanoid(),
			conversationId: convId,
			message: answer,
			createdAt: new Date(),
			role: role as 'user' | 'system' | 'assistant'
		}

		const addedMessage = (await db.insert(table.message).values(newMessage).returning()).at(0);

		if(!addedMessage){
			throw Error('Error initializing conversation');
		}

		return addedMessage;
	}

	static async deleteConversation(userId: string, convId: string): Promise<void> {

		const tmp = (await db.select().from(table.conversation)
			.where(eq(conversation.id, convId))).at(0)

		if(!tmp) {
			throw Error('Error initializing conversation');
		}

		if(tmp.userId !== userId){
			throw Error('Error initializing conversation');
		}

		await db.delete(table.message).where(eq(message.conversationId, convId))
		await db.delete(table.conversation).where(eq(conversation.id, convId))

	}
}