import type { ConversationWithMessages } from '$lib/types';
import { nanoid } from 'nanoid';
import { db } from '$lib/server/db';
import * as table from "$lib/server/db/schema";
import {eq} from "drizzle-orm";
import { conversation, type Conversation, type Message, message, context, type Context } from '$lib/server/db/schema';



export class ConversationService {

	static async initConversation(name: string, userId: string): Promise<Conversation> {
		console.log('Initializing conversation:', name, 'for user:', userId);
		
		const newConversation = {
			id: nanoid(),
			name: name,
			userId: userId,
			createdAt: new Date(),
			updatedAt: new Date(),
		}

		try {
			const tmpConversation = await db.insert(table.conversation).values(newConversation).returning()
			const result = tmpConversation.at(0) as Conversation;
			console.log('Conversation created:', result);
			return result;
		} catch (error) {
			console.error('Error creating conversation:', error);
			throw Error('Failed to create conversation');
		}
	}

	static async getUserConversation(userId: string): Promise<Conversation[]> {
		return db.select().from(table.conversation)
			.where(eq(conversation.userId, userId))
	}

	static async getConversation(id: string): Promise<ConversationWithMessages> {
		console.log('Getting conversation with id:', id);
		
		const tmpConversation = (await db.select().from(table.conversation)
			.where(eq(conversation.id, id))).at(0);

		if(!tmpConversation){
			console.log('Conversation not found with id:', id);
			throw Error('Conversation not found');
		}

		console.log('Found conversation:', tmpConversation);

		const messages = await db.select().from(table.message)
			.where(eq(message.conversationId, tmpConversation.id))

		const contexts = await db.select().from(table.context)
			.where(eq(context.conversationId, tmpConversation.id))

		return {
			...tmpConversation,
			messages: messages,
			contexts: contexts
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
		console.log('Deleting conversation:', convId, 'for user:', userId);

		const tmp = (await db.select().from(table.conversation)
			.where(eq(conversation.id, convId))).at(0)

		if(!tmp) {
			console.log('Conversation not found for deletion:', convId);
			throw Error('Conversation not found');
		}

		if(tmp.userId !== userId){
			console.log('User not authorized to delete conversation:', userId, 'conversation belongs to:', tmp.userId);
			throw Error('Not authorized to delete this conversation');
		}

		console.log('Deleting messages for conversation:', convId);
		await db.delete(table.message).where(eq(message.conversationId, convId))
		
		console.log('Deleting conversation:', convId);
		await db.delete(table.conversation).where(eq(conversation.id, convId))
	}

	static async addContext(conversationId: string, content: string, sources: string[] = []): Promise<Context> {
		const newContext = {
			id: nanoid(),
			conversationId,
			content,
			sources: JSON.stringify(sources),
			createdAt: new Date()
		}

		const addedContext = (await db.insert(table.context).values(newContext).returning()).at(0);

		if(!addedContext){
			throw Error('Error adding context');
		}

		return addedContext;
	}

	static async getContexts(conversationId: string): Promise<Context[]> {
		return db.select().from(table.context)
			.where(eq(context.conversationId, conversationId))
	}
}