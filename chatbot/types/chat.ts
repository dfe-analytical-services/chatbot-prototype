export type Message = {
    type: 'apiMessage' | 'userMessage';
    message: string;
    isStreaming?: boolean;
    links?: string[];
}