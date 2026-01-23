import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';
import { env } from '$env/dynamic/private';

if (!env.DB) throw new Error('DB is not set');

const client = postgres(env.DB);

export const db = drizzle(client, { schema });
