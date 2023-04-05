import { useRef, useState, useEffect, useMemo, useCallback } from 'react';
import Layout from '@/components/layout';
import styles from '@/styles/Home.module.css';
import {Message} from '@/types/chat';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import LoadingDots from '@/components/ui/LoadingDots';
import { Document } from 'langchain/document';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

export default function Home() {
    const [query, setQuery] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [sourceDocs, setSourceDocs] = useState<Document[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [messageState, setMessageState] = useState<{
        messages: Message[];
        pending?: string;
        pendingSourceDocs?: Document[];
    }>({
        messages: [
            {
                message: "Hi what would you like to learn about the document?",
                type: 'apiMessage',
            },
        ],
                pendingSourceDocs: [],
    });

    const {messages, pending, pendingSourceDocs} = messageState;

    const messageListRef = useRef<HTMLDivElement>(null);
    const textAreaRef = useRef<HTMLTextAreaElement>(null);
    
    useEffect(() => {
        textAreaRef.current?.focus();
      }, []);
    
      //handle form submission
      async function handleSubmit(e: any) {
        e.preventDefault();
    
        setError(null);
    
        if (!query) {
          alert('Please input a question');
          return;
        }
    
        const question = query.trim();
    
        setMessageState((state) => ({
          ...state,
          messages: [
            ...state.messages,
            {
              type: 'userMessage',
              message: question,
            },
          ],
          pending: undefined,
        }));

        //reset the query and parameter variables
        setLoading(true);
        setQuery('');
        setMessageState((state) => ({ ...state, pending: '' }));
    }
    //NEED TO UNDERSTAND AND EXPLAIN FROM HERE

}