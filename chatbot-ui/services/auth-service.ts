import { headers } from 'next/headers';

export const isAuthenticated = () => {
  const authorization = headers().get('authorization');

  if (!authorization) {
    return false;
  }

  const authValue = authorization.split(' ')[1];
  const [username, password] = atob(authValue).split(':');

  return username == 'dfe' && password == process.env.AUTH_PASSWORD;
};
