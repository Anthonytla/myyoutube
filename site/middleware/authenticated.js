export default async function ({$auth, redirect}) {
  // If the user is not authenticated
  if (!$auth.loggedIn) {
    //let the user in
    return redirect('/login')
  }
}

/*export default function({ redirect, store }) {
  const isAuthenticated = store.state.auth.user ? true : false
  if (!isAuthenticated) {
    redirect('/login')
  }
}*/
