export function useAuth() {
  const supabase = useSupabaseClient();
  const router = useRouter();
  const errorMessage = ref('');

  const signIn = async (email, password) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = '';
      router.push('/');
    }
  };
  
  const signUp = async (email: string, password: string) => {
    const { user, error } = await supabase.auth.signUp({ email, password });
    if (error) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = '';
    }
  };

  return {
    signIn,
    signUp,
    errorMessage
  };
}
