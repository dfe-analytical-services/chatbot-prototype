export interface EESCredential {
  username: string;
  password: string;
}

const authenticateCredentials = (credential: EESCredential) => {
  if (
    credential.username === process.env.NEXT_PUBLIC_AUTH_USERNAME &&
    credential.password === process.env.NEXT_PUBLIC_AUTH_PASSWORD
  ) {
    return true;
  }

  return false;
};

export default authenticateCredentials;
