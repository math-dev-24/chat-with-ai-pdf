import { sqliteTable, integer, text } from 'drizzle-orm/sqlite-core';

export const user = sqliteTable('user', {
	id: text('id').primaryKey(),
	age: integer('age'),
	username: text('username').notNull(),
	password: text('password').notNull(),
});

export const session = sqliteTable('session', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => user.id),
	expiresAt: integer('expires_at', { mode: 'timestamp' }).notNull()
});


export const conversation = sqliteTable('conversation', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	userId: text('user_id')
	.notNull()
	.references(() => user.id),
	createdAt: integer('createdAt', {mode: 'timestamp' }).notNull(),
	updatedAt: integer('updatedAt', {mode: 'timestamp' }).notNull(),
})

export const message = sqliteTable('message', {
	id: text('id').primaryKey(),
	conversationId: text('conversation_id')
		.notNull()
		.references(() => conversation.id, { onDelete: 'cascade' }),
	role: text('role', {enum: ['user', 'system', 'assistant']}).notNull(),
	message: text('message').notNull(),
	createdAt: integer('created_at', { mode: 'timestamp' }).notNull()
})

export const context = sqliteTable('context', {
	id: text('id').primaryKey(),
	conversationId: text('conversation_id')
		.notNull()
		.references(() => conversation.id, { onDelete: 'cascade' }),
	content: text('content').notNull(),
	sources: text('sources').notNull().default('[]'),
	createdAt: integer('created_at', { mode: 'timestamp' }).notNull()
})

export type Session = typeof session.$inferSelect;
export type User = typeof user.$inferSelect;
export type Conversation = typeof conversation.$inferSelect;
export type Message = typeof message.$inferSelect;
export type Context = typeof context.$inferSelect;