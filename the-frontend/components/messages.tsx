import { Message } from "ai/react/dist";
import { Card, CardBody } from "@nextui-org/card"
import { motion } from "framer-motion";
import RenderMarkdown from "./renderMarkdown";
import { useEffect, useRef } from "react";
import ThinkingText from "./thinkingText";


interface MessagesProps {
  messages: Message[]
}

interface IndividualMessage {
  message: Message;
}

const UserMessage: React.FC<IndividualMessage> = ({ message }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 20
      }}
      className="flex justify-end w-full"
    >
      <Card className="bg-blue-500 text-white rounded-lg shadow-md my-2 max-w-[50%]">
        <CardBody>
          <RenderMarkdown content={message.content} speed={1} useTextAnimation={false} />
        </CardBody>
      </Card>
    </motion.div>
  );
};


const SystemMessage: React.FC<IndividualMessage> = ({ message }) => {
  if (message.content === "") {
    return null;
  }
  return (
    <motion.div
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 20
      }}
      className="flex justify-start w-full"
    >
      <Card className="rounded-lg shadow-md my-2 w-max">
        <CardBody>
          <RenderMarkdown content={message.content} speed={1} useTextAnimation={true} />
        </CardBody>
      </Card>
    </motion.div>
  );
};

const Messages: React.FC<MessagesProps> = ({ messages }) => {

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: "smooth",
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col pb-60">
      {messages.map((message, index) => {
        if (message.role === 'user') {
          return <UserMessage key={index} message={message} />
        }
        return <SystemMessage key={index} message={message} />
      })}
      {messages.length > 0 && ((messages[messages.length - 1].role === 'user') || (messages[messages.length - 1].content === "")) ? <ThinkingText /> : null}
      <div ref={messagesEndRef} />
    </div>
  );
};
export default Messages;