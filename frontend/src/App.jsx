import React,{useEffect,useState} from 'react';
import {api,downloadFile} from './services/api';
import './styles.css';

function Auth({onLogin}){
 const [mode,setMode]=useState('login'),[form,setForm]=useState({name:'',email:'',password:'',role:'student'}),[error,setError]=useState('');
 async function submit(e){e.preventDefault();setError('');try{const d=await api(`/api/${mode==='login'?'login':'register'}`,{method:'POST',body:form});onLogin(d)}catch(e){
  if (Array.isArray(e?.detail)) {
    setError(e.detail.map(x => x.msg || JSON.stringify(x)).join(", "));
  } else if (e?.detail) {
    setError(String(e.detail));
  } else {
    setError(e?.message || "Something went wrong");
  }
}}
 return <div className="auth"><div className="card"><h1>Assignment Portal</h1><p className="muted">Cloud Computing Project</p><div className="tabs"><button className={mode==='login'?'active':''} onClick={()=>setMode('login')}>Login</button><button className={mode==='register'?'active':''} onClick={()=>setMode('register')}>Register</button></div><form onSubmit={submit}>{mode==='register'&&<input placeholder="Full name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>}<input type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/><input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>{mode==='register'&&<select value={form.role} onChange={e=>setForm({...form,role:e.target.value})}><option value="student">Student</option><option value="teacher">Teacher</option></select>}<button className="primary">{mode==='login'?'Login':'Create account'}</button>{error&&<p className="error">{error}</p>}</form></div></div>
}
function Layout({user,onLogout,children}){return <><header><b>☁ Assignment Portal</b><span>{user.name} · {user.role}</span><button onClick={onLogout}>Logout</button></header><main>{children}</main></>}
function Student({token}){
 const [assignments,setAssignments]=useState([]),[subs,setSubs]=useState([]),[msg,setMsg]=useState('');
 async function load(){setAssignments(await api('/api/assignments',{token}));setSubs(await api('/api/submissions/me',{token}))}; useEffect(()=>{load()},[]);
 async function upload(a,file){if(!file)return;setMsg('Uploading...');try{const fd=new FormData();fd.append('file',file);await api(`/api/assignments/${a.id}/submit`,{method:'POST',token,body:fd,form:true});setMsg('Submission saved.');load()}catch(e){setMsg(e.message)}}
 const subBy=a=>subs.find(s=>s.assignment_id===a.id);
 return <div><h2>Student Dashboard</h2><div className="grid"><Stat title="Assignments" value={assignments.length}/><Stat title="Submitted" value={subs.length}/><Stat title="Graded" value={subs.filter(s=>s.submission_status==='GRADED').length}/></div><p className="notice">{msg}</p><section className="card"><h3>Assignments</h3>{assignments.map(a=>{const s=subBy(a);return <div className="item" key={a.id}><div><b>{a.title}</b><p>{a.description}</p><small>Deadline: {new Date(a.deadline).toLocaleString()} · Max: {a.max_marks}</small>{s&&<p>Status: <b>{s.submission_status}</b> {s.marks!==null&&`· ${s.marks}/${a.max_marks}`} {s.feedback&&<span>· Feedback: {s.feedback}</span>}</p>}</div><label className="upload">{s?'Resubmit':'Upload'}<input type="file" hidden onChange={e=>upload(a,e.target.files[0])}/></label>{s&&<button onClick={()=>downloadFile(s.id,token,s.file_name)}>Download</button>}</div>})}</section></div>
}
function Teacher({token}){
 const [courses,setCourses]=useState([]);
 const [assignments,setAssignments]=useState([]);
 const [subs,setSubs]=useState([]);
 const [courseName,setCourseName]=useState('');
 const [form,setForm]=useState({
   course_id:'',
   title:'',
   description:'',
   deadline:'',
   max_marks:100,
   allowed_file_types:'pdf,docx,zip',
   max_file_size_mb:10
 });
 const [msg,setMsg]=useState('');

 async function load(){
   try{
     const [c,a]=await Promise.all([
       api('/api/courses',{token}),
       api('/api/assignments',{token})
     ]);

     setCourses(c);
     setAssignments(a);

     let all=[];
     for(const x of a){
       const ss=await api(`/api/assignments/${x.id}/submissions`,{token});
       all=all.concat(ss);
     }
     setSubs(all);
   }catch(e){
     setMsg(e.message);
   }
 }

 useEffect(()=>{
   load();
 },[]);

 async function createCourse(e){
   e.preventDefault();

   if(!courseName.trim()){
     setMsg('Please enter a course name.');
     return;
   }

   try{
     await api('/api/courses',{
       method:'POST',
       token,
       body:{course_name:courseName.trim()}
     });

     setCourseName('');
     setMsg('Course created successfully.');
     load();
   }catch(e){
     setMsg(e.message);
   }
 }

 async function create(e){
   e.preventDefault();

   if(!form.course_id){
     setMsg('Please select a course.');
     return;
   }

   try{
     await api('/api/assignments',{
       method:'POST',
       token,
       body:{
         ...form,
         course_id:Number(form.course_id)
       }
     });

     setMsg('Assignment created.');
     setForm({
       ...form,
       title:'',
       description:''
     });

     load();
   }catch(e){
     setMsg(e.message);
   }
 }

 async function grade(s){
   const marks=prompt('Marks');
   if(marks===null)return;

   const feedback=prompt('Feedback')||'';

   try{
     await api(`/api/submissions/${s.id}/grade`,{
       method:'POST',
       token,
       body:{
         marks:Number(marks),
         feedback
       }
     });

     load();
   }catch(e){
     setMsg(e.message);
   }
 }

 return <div>
   <h2>Teacher Dashboard</h2>

   <div className="grid">
     <Stat title="Courses" value={courses.length}/>
     <Stat title="Assignments" value={assignments.length}/>
     <Stat title="Submissions" value={subs.length}/>
     <Stat title="Pending Reviews" value={subs.filter(s=>s.submission_status!=='GRADED').length}/>
   </div>

   <p className="notice">{msg}</p>

   <section className="card">
     <h3>Create Course</h3>

     <form className="formgrid" onSubmit={createCourse}>
       <input
         placeholder="Course name"
         value={courseName}
         onChange={e=>setCourseName(e.target.value)}
       />

       <button className="primary">
         Create Course
       </button>
     </form>
   </section>

   <section className="card">
     <h3>Your Courses</h3>

     {courses.length===0 ? (
       <p className="muted">No courses created yet.</p>
     ) : (
       courses.map(c=>(
         <div className="item" key={c.id}>
           <div>
             <b>{c.course_name}</b>
           </div>
         </div>
       ))
     )}
   </section>

   <section className="card">
     <h3>Create Assignment</h3>

     <form className="formgrid" onSubmit={create}>
       <input
         placeholder="Title"
         value={form.title}
         onChange={e=>setForm({...form,title:e.target.value})}
       />

       <input
         type="datetime-local"
         value={form.deadline}
         onChange={e=>setForm({...form,deadline:e.target.value})}
       />

       <textarea
         placeholder="Description"
         value={form.description}
         onChange={e=>setForm({...form,description:e.target.value})}
       />

       <input
         type="number"
         value={form.max_marks}
         onChange={e=>setForm({...form,max_marks:Number(e.target.value)})}
       />

       <select
         value={form.course_id}
         onChange={e=>setForm({...form,course_id:e.target.value})}
       >
         <option value="">Select course</option>

         {courses.map(c=>(
           <option key={c.id} value={c.id}>
             {c.course_name}
           </option>
         ))}
       </select>

       <button className="primary">
         Create Assignment
       </button>
     </form>
   </section>

   <section className="card">
     <h3>Submissions</h3>

     {subs.map(s=>(
       <div className="item" key={s.id}>
         <div>
           <b>Submission #{s.id}</b>
           <p>{s.file_name} · {s.submission_status}</p>
           <small>
             {new Date(s.submitted_at).toLocaleString()}
           </small>
         </div>

         <button onClick={()=>downloadFile(s.id,token,s.file_name)}>
           Download
         </button>

         {s.submission_status!=='GRADED'&&
           <button onClick={()=>grade(s)}>
             Grade
           </button>
         }

         {s.feedback&&
           <span>
             {s.marks} · {s.feedback}
           </span>
         }
       </div>
     ))}
   </section>
 </div>
}
function Stat({title,value}){return <div className="stat"><span>{title}</span><strong>{value}</strong></div>}
export default function App(){const [session,setSession]=useState(()=>JSON.parse(localStorage.getItem('portal_session')||'null'));function login(d){localStorage.setItem('portal_session',JSON.stringify(d));setSession(d)}function logout(){localStorage.removeItem('portal_session');setSession(null)}if(!session)return <Auth onLogin={login}/>;return <Layout user={session.user} onLogout={logout}>{session.user.role==='teacher'?<Teacher token={session.access_token}/>:<Student token={session.access_token}/>}</Layout>}
