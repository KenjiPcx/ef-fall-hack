import React, { useEffect, useState } from 'react';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark-dimmed.css'; // For code highlighting
import ReactMarkdown from 'react-markdown';

interface RenderMarkdownProps {
  content: string;
  speed: number;
  useTextAnimation: boolean;
}

const RenderMarkdown: React.FC<RenderMarkdownProps> = ({ content, speed, useTextAnimation }) => {

  const [displayedContent, setDisplayedContent] = useState('');
  useEffect(() => {
    // Reset displayed content when content changes
    setDisplayedContent('');
  }, [content]);

  useEffect(() => {
    // If all content is already displayed, do nothing
    if (displayedContent.length >= content.length) return;

    // Use requestAnimationFrame for smoother, more consistent rendering
    let animationFrameId: number;
    let lastTime = 0;

    const animate = (currentTime: number) => {
      // Only add a character if enough time has passed
      if (currentTime - lastTime >= speed) {
        setDisplayedContent(prev => {
          // Ensure we don't exceed original content length
          const nextContent = content.slice(0, prev.length + 1);
          return nextContent;
        });
        lastTime = currentTime;
      }

      // Continue animation if not all characters are displayed
      if (displayedContent.length < content.length) {
        animationFrameId = requestAnimationFrame(animate);
      }
    };

    // Start the animation
    animationFrameId = requestAnimationFrame(animate);

    // Cleanup function
    return () => {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [content, displayedContent, speed]);


  return (
    <ReactMarkdown
      rehypePlugins={[rehypeHighlight]}
      components={{
        h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-2" {...props} />,
        h2: ({ node, ...props }) => <h2 className="text-xl font-semibold mb-2" {...props} />,
        a: ({ node, ...props }) => (
          <a
            className="text-white underline hover:text-blue-200"
            target="_blank"
            rel="noopener noreferrer"
            {...props}
          />
        ),
        code: ({ node, className, children, ...props }) => (
          <code
            className={`text-white rounded px-1 py-0.5 text-sm ${className}`}
            {...props}
          >
            {children}
          </code>
        ),
        pre: ({ node, children, ...props }) => (
          <pre
            className="text-white rounded p-2 overflow-x-auto text-sm"
            {...props}
          >
            {children}
          </pre>
        )
      }}
    >
      {useTextAnimation ? displayedContent : content}
    </ReactMarkdown>
  );
};

export default RenderMarkdown;