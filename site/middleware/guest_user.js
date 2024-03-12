export default async function ({$auth, redirect}) {
  // If the user is not authenticated
  if ($auth.loggedIn) {
    return redirect('/')
  }
}

/*export default function({ redirect, store }) {
  const isAuthenticated = store.state.auth.user ? true : false
  if (isAuthenticated) {
    redirect('/')
  }
}*/

/*export default function ({ store, redirect }) {
  if (store.state.auth.user) {
    return redirect('/')
  }
}*/