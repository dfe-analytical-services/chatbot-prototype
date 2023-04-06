import type { NextApiRequest, NextApiResponse } from 'next';
import { openai } from '@/utils/openai-client'
import { OpenAIEmbeddings } from 'langchain/embeddings';
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const response = await openai.call('Hello, how can I help you?');
    res.status(200).json({ data: response });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
