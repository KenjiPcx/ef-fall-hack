import { Message } from "ai/react/dist";

export const exampleMessages: Message[] = [
  {
    id: '1',
    createdAt: new Date('2023-10-01T10:00:00Z'),
    content: 'Hello, how can I assist you today?',
    role: 'assistant',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '2',
    createdAt: new Date('2023-10-01T10:01:00Z'),
    content: 'I need some information about your services.',
    role: 'user',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '3',
    createdAt: new Date('2023-10-01T10:02:00Z'),
    content: 'Sure, we offer a variety of services including web development, mobile app development, and AI solutions.',
    role: 'assistant',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '4',
    createdAt: new Date('2023-10-01T10:03:00Z'),
    content: 'Can you tell me more about your AI solutions?',
    role: 'user',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '5',
    createdAt: new Date('2023-10-01T10:04:00Z'),
    content: 'Our AI solutions include natural language processing, computer vision, and predictive analytics. We tailor our solutions to meet the specific needs of our clients.',
    role: 'assistant',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '6',
    createdAt: new Date('2023-10-01T10:04:00Z'),
    content: 'KLCC Image: ![KLCC](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-cRStZbP8hex-CWagOcxF2mDoAP71P3z7nQ&s)',
    role: 'assistant',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '7',
    createdAt: new Date('2023-10-01T10:04:00Z'),
    content: 'KLCC Image: ![KLCC](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-cRStZbP8hex-CWagOcxF2mDoAP71P3z7nQ&s)',
    role: 'user',
    annotations: [],
    toolInvocations: []
  },
  {
    id: '8',
    createdAt: new Date('2023-10-01T10:02:00Z'),
    content: 'Sure, here is an example of a Python code block:\n\n```python\n# This is a simple Python function\ndef greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("World"))\n```',
    role: 'assistant',
    annotations: [],
    toolInvocations: []
  },
];
