import { renderHook } from '@testing-library/react';
import useChatbot from './useChatbot';

describe('useChatbot', () => {
  it('Initialises', () => {
    const { result } = renderHook(() => useChatbot());

    const { messages } = result.current;

    expect(messages).toHaveLength(1);
  });

  // TODO: Test this hook more, especially async behaviour
});
