import { exampleMessages } from '@/components/example_messages';
import Messages from '@/components/messages';
import { Textarea } from '@nextui-org/input';
import { useChat } from 'ai/react'
import { useEffect } from 'react';
import { Button } from '@nextui-org/button';
import SendIcon from '@/icons/sendIcon';


export default function IndexPage() {
  const { messages, input, handleSubmit, handleInputChange, isLoading } = useChat({
    api: `http://localhost:8000/api/chat`,
    initialMessages: []
  });

  const handleSubmitTextArea = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);

    }
  }

  useEffect(() => {
    console.log(messages);
  }, [messages])

  return (
    <div className="container mx-auto px-4">

      <Messages messages={messages} />

      <div className="fixed bottom-4 container mx-auto px-4">

      <Textarea
        placeholder="Type something..."
        autoFocus
        fullWidth
        rows={3}
        variant="faded"
        value={input}
        onChange={handleInputChange}
        disabled={isLoading}
        onKeyDown={handleSubmitTextArea}
        />
      
        <Button
          className="absolute w-10 h-10 right-6 bottom-2 bg-blue-500 text-white rounded-full z-10"
          onClick={() => handleSubmit()}
          disabled={isLoading || input.length === 0}
          isIconOnly
        >
          <SendIcon enabled={!isLoading && input.length > 0} />
        </Button>
      </div>


    </div>
  )
}
