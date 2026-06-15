export function MessageBubble({ role, content }: { role: string; content: string }) {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div className={`max-w-[70%] rounded-lg px-4 py-2 ${
        isUser ? 'bg-blue-600 text-white' : 'bg-white border border-gray-200 text-gray-800'
      }`}>
        <p className="whitespace-pre-wrap">{content}</p>
      </div>
    </div>
  );
}
