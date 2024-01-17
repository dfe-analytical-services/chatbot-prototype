import { NextResponse } from 'next/server';
import { isAuthenticated } from '@/services/auth-service';

export function middleware() {
  if (isAuthenticated()) {
    return NextResponse.next();
  }

  // Respond with JSON indicating an error message
  return new NextResponse('Authentication required', {
    status: 401,
    headers: { 'WWW-Authenticate': 'Basic realm="Secure Area"' },
  });
}

// Define matching paths
export const config = {
  matcher: '/',
};
