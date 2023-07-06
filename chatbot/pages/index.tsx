import { useRef, useState, useEffect} from 'react';
import Layout from '@/components/layout';
import styles from '@/styles/Home.module.css';
import Link from 'next/link';
import {Message} from '@/types/chat';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import LoadingDots from '@/components/ui/LoadingDots';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';



//import {Layout} from 'govuk-frontend';

export default function Home() {
  const [query, setQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [messageState, setMessageState] = useState<{ 
    messages: Message[];
    history: [string, string][];
    pending?: string;
  }>({
    messages: [
      {
        message: 'Hi, what would you like to know about the latest publications on EES?',
        type: 'apiMessage',
      },
    ],
    history: [],
  });

  const { messages, history } = messageState;
  

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
    }));

    setLoading(true);
    setQuery('');

    let pending = '';

    try {
      const response = await fetch('http://localhost:8000/api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question,
          history
        }),
      });

      const data = await response.body;
      
      setMessageState((state) =>({
        history: [...state.history],
        messages: [
          ...state.messages, {
            type: 'apiMessage',
            message: '',
          }
        ]
      }))

      if(!data){
        return;
      }

      const reader = data.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done){
        const {value, done: doneReading} = await reader.read()
        done = doneReading;
        const chunkValue = decoder.decode(value);
        if (chunkValue.startsWith('{"sourceDocuments":')){
          setMessageState((state) => {
            let messages = state.messages;
            messages[messages.length - 1].links = JSON.parse(chunkValue).sourceDocuments
            return {...state, messages: [...messages]};
          })
        } else{
          pending += chunkValue;
          setMessageState((state) => {
            let messages = state.messages;
            messages[messages.length-1].message = pending;
            return {...state, messages: [...messages]};
          });
      }
    }
      setLoading(false);

      //scroll to bottom
      //messageListRef.current?.scrollTo(0, messageListRef.current.scrollHeight);
    } catch (error) {
      setLoading(false);
      setError('An error occurred while fetching the data. Please try again.');
      console.log('error', error);
    }
  }

  //prevent empty submissions
  const handleEnter = (e: any) => {
    if (e.key === 'Enter' && query) {
      handleSubmit(e);
    } else if (e.key == 'Enter') {
      e.preventDefault();
    }
  };

      return (
      <>
          <Layout>


            <div>

              <main className={styles.main}>
                <div className={`${styles.cloud} govuk-clearfix`}>
                  <div ref={messageListRef} className={styles.messagelist}>
                   <Link href='/' >
                    Go back to homepage
                    <div className='govuk-link'>

                    </div>
                   </Link>
                    {messages.map((message, index) => {
                      let icon;
                      let className;
                     
                     if (message.type === 'apiMessage') {
                        icon = (
                          <Image
                            src="/govuk-logo.png"
                            alt="AI"
                            width="40"
                            height="40"
                            className={styles.boticon}
                            priority
                          />
                        );
                        className = styles.apimessage;
                      } else {
                        icon = (
                          <Image
                            src="/dfe.png"
                            alt="Me"
                            width="30"
                            height="30"
                            className={styles.usericon}
                            priority
                          />
                        );
                        // The latest message sent by the user will be animated while waiting for a response
                        className =
                          loading && index === messages.length - 1
                            ? styles.usermessagewaiting
                            : styles.usermessage;
                      }  return (
                        <>
                          <div key={`chatMessage-${index}`} className={className}>
                            {icon}
                            <div className={styles.markdownanswer}>
                              <ReactMarkdown linkTarget="_blank">
                                {message.message}
                              </ReactMarkdown>
                            </div>
                          </div>
                      
                        { /*{ message.links && (
                            <div className="p-5">
                              <Accordion
                                type="single"
                                collapsible
                                className="flex-col"
                              >
                                {message.links.map((doc, index) => (
                                  <div key={`messagelinks-${index}`}>
                                    <AccordionItem value={`item-${index}`}>
                                      <AccordionTrigger>
                                        <h3>Related publication {index + 1}</h3>
                                      </AccordionTrigger>
                                      <AccordionContent>
                                        <p className="mt-2">
                                        <a href={doc}>{doc}</a>
                                        </p>
                                      </AccordionContent>
                                    </AccordionItem>
                                  </div>
                                ))}
                              </Accordion>
                            </div>
                                )} */ }
                        </>
                      );
                    })}
                  </div>
                </div>
                <div className={styles.center}>
                  <div className={styles.cloudform}>
                    <form onSubmit={handleSubmit}>
                      <textarea
                        disabled={loading}
                        onKeyDown={handleEnter}
                        ref={textAreaRef}
                        autoFocus={false}
                        rows={1}
                        maxLength={5000}
                        id="userInput"
                        name="userInput"
                        placeholder={
                          loading
                            ? 'Waiting for response...'
                            : 'Ask a question here'
                        }
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className={styles.textarea}
                      />
                      <button
                        type="submit"
                        disabled={loading}
                        className={styles.generatebutton}
                      >
                        {loading ? (
                          <div className={styles.loadingwheel}>
                            <LoadingDots color="#000" />
                          </div>
                        ) : (
                          // Send icon SVG in input field
                          <svg
                            viewBox="0 0 20 20"
                            className={styles.svgicon}
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
                          </svg>
                        )}
                      </button>
                    </form>
                  </div>
                </div>
                {error && (
                  <div className="border border-red-400 rounded-md p-4">
                    <p className="text-red-500">{error}</p>
                  </div>
                )}
              </main>
              </div>
          </Layout>
        </>
      );
    }