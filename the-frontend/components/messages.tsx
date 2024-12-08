// @ts-nocheck
import { Message } from "ai/react/dist";
import { Card, CardBody } from "@nextui-org/card"
import { motion } from "framer-motion";
import RenderMarkdown from "./renderMarkdown";
import { useEffect, useRef } from "react";
import ThinkingText from "./thinkingText";
import { Spinner } from "@nextui-org/spinner"

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

type TaskDictReturn = {
  [dict_key: string]: string;
};

function isJSONObject(value: any) {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function getTasksDict(message: Message): TaskDictReturn {
  let tasksDict = { 'Analyst': 0, 'Researcher': 0, 'Research Manager': 0 };
  if (message.annotations) {
    for (const annotation of message.annotations) {
      if (isJSONObject(annotation)) {
        if ("type" in annotation && annotation["type"] === "agent" && "data" in annotation && "text" in annotation["data"]) {
          if (annotation["data"]["text"] === "Finished task") {
            if (annotation["data"]["agent"] in tasksDict) {
              tasksDict[annotation["data"]["agent"]] += 1
            } else {
              tasksDict[annotation["data"]["agent"]] = 1
            }
          }
        }
      }
    }
  }
  return tasksDict;
}

const SystemMessage: React.FC<IndividualMessage> = ({ message }) => {
  const tasksDict = message.annotations ? getTasksDict(message) : {};

  return (
    <>
      {Object.keys(tasksDict).map((agent, index) => (
        <div key={index} className="flex items-center space-x-2 mb-2">
          <div className="flex items-center space-x-2 mb-2">
            <Spinner size="sm" />
            <span>{tasksDict[agent]} {agent} tasks completed</span>
          </div>
        </div>
      ))}
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
          {message.content === "" ? null : <RenderMarkdown content={message.content} speed={1} useTextAnimation={true} />}
        </CardBody>
      </Card>
    </motion.div>
      </>
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