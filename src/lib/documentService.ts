import { supabase } from '@/lib/supabaseClient';

export async function saveDocument(input: {
  title: string;
  template: string;
  content: string;
}) {
  const { data: sessionData } = await supabase.auth.getSession();
  const userId = sessionData.session?.user.id;

  if (!userId) {
    return { error: 'No active session' };
  }

  const { data, error } = await supabase
    .from('documents')
    .insert({
      title: input.title,
      template: input.template,
      content: input.content,
      owner_id: userId,
      status: 'draft'
    })
    .select()
    .single();

  if (error) {
    return { error: error.message };
  }

  return { data };
}

export async function listDocuments() {
  const { data, error } = await supabase
    .from('documents')
    .select('id,title,template,status,created_at')
    .order('created_at', { ascending: false });

  if (error) {
    return { error: error.message, data: [] };
  }

  return { data: data || [] };
}
