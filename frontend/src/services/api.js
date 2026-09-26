const API=import.meta.env.VITE_API_URL||'http://localhost:8000';
export async function api(path,{method='GET',body,token,form=false}={}){
 const headers={}; if(token) headers.Authorization=`Bearer ${token}`; if(body && !form) headers['Content-Type']='application/json';
 const r=await fetch(`${API}${path}`,{method,headers,body:form?body:body?JSON.stringify(body):undefined});
 const data=await r.json().catch(()=>({detail:r.statusText})); if(!r.ok) throw new Error(data.detail||'Request failed'); return data;
}
export async function downloadFile(id,token,name){
 const r=await fetch(`${API}/api/submissions/${id}/download`,{headers:{Authorization:`Bearer ${token}`}}); if(!r.ok) throw new Error('Download failed');
 const blob=await r.blob(), a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name||'submission'; a.click(); URL.revokeObjectURL(a.href);
}
export {API};
