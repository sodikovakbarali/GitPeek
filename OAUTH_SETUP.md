# 🔐 GitHub OAuth Setup Guide

## ⚡ TL;DR - OAuth is OPTIONAL!

**GitPeek works perfectly WITHOUT OAuth!** You can:
- ✅ Search any GitHub user
- ✅ View all public repositories
- ✅ See all public commits
- ✅ View activity charts
- ✅ Use all main features

**OAuth is only needed if you want to:**
- 🔒 View your own private repositories
- 🔒 See commits to private repos you have access to
- 🔒 View private repos of organizations you belong to

**Most users can skip this guide completely!**

---

## 🚀 Quick Start (No OAuth)

```bash
# Clone and run - works immediately!
git clone <repo-url>
cd GitPeek
docker-compose up -d
```

Open http://localhost:3000 and start searching! 🎉

---

## 🔐 When Do You Need OAuth?

### You DON'T need OAuth if:
- ✅ You only want to view public repositories
- ✅ You're searching other users (not yourself)
- ✅ You don't care about private repos

### You DO need OAuth if:
- 🔒 You want to see YOUR private repositories
- 🔒 You want to see commits to private repos
- 🔒 You're part of private organizations and want to see that activity

---

## 📋 Complete OAuth Setup Guide

**Time Required:** 5-10 minutes
**Difficulty:** Easy - just follow the steps!

### Prerequisites

- A GitHub account
- GitPeek already cloned and running (without OAuth)

---

## Step 1: Create a GitHub OAuth Application

### 1.1 Go to GitHub Developer Settings

Open your browser and go to:
```
https://github.com/settings/developers
```

Or navigate manually:
1. Click your profile picture (top right on GitHub)
2. Click **Settings**
3. Scroll down to **Developer settings** (bottom left)
4. Click **OAuth Apps**

### 1.2 Create New OAuth App

Click the **"New OAuth App"** button (or "Register a new application")

### 1.3 Fill in the Application Details

Enter the following information **exactly as shown**:

| Field | Value | Notes |
|-------|-------|-------|
| **Application name** | `GitPeek` | Or any name you prefer |
| **Homepage URL** | `http://localhost:3000` | For local development |
| **Application description** | `GitPeek - View GitHub Activity` | Optional |
| **Authorization callback URL** | `http://localhost:3000/auth/callback` | ⚠️ **MUST BE EXACT** |

⚠️ **IMPORTANT:** The callback URL must be **EXACTLY** `http://localhost:3000/auth/callback`

### 1.4 Register the Application

Click **"Register application"**

---

## Step 2: Get Your OAuth Credentials

After creating the app, you'll see your application page.

### 2.1 Copy Your Client ID

You'll see:
```
Client ID: abc123def456...
```

**Copy this value** - you'll need it in a moment.

### 2.2 Generate a Client Secret

1. Find the section labeled **"Client secrets"**
2. Click **"Generate a new client secret"**
3. GitHub may ask for your password - enter it
4. **IMMEDIATELY COPY THE SECRET** - you won't see it again!

⚠️ **IMPORTANT:** Copy the secret immediately! GitHub only shows it once.

Your secret looks like: `1234567890abcdef1234567890abcdef12345678`

---

## Step 3: Configure GitPeek

Now you need to add these credentials to GitPeek.

### 3.1 Navigate to Your GitPeek Directory

```bash
cd /path/to/GitPeek
```

### 3.2 Create the .env File

Create a file named `.env` in the root directory:

```bash
# Linux/Mac
nano .env

# Or use any text editor
```

### 3.3 Add Your Credentials

Copy and paste this template into `.env`:

```bash
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback

# Security Key (can leave as-is or generate your own)
SECRET_KEY=change-this-to-a-secure-random-key
```

### 3.4 Replace the Placeholder Values

Replace `your_client_id_here` and `your_client_secret_here` with your actual values:

```bash
# Example (use YOUR values!)
GITHUB_CLIENT_ID=abc123def456ghi789
GITHUB_CLIENT_SECRET=1234567890abcdef1234567890abcdef12345678
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
SECRET_KEY=my-super-secret-key-12345
```

### 3.5 Save the File

- **nano:** Press `Ctrl+X`, then `Y`, then `Enter`
- **Other editors:** Save and close

---

## Step 4: Restart GitPeek Backend

Now restart the backend to load the new configuration:

```bash
# Restart just the backend
docker-compose restart backend

# Or restart everything
docker-compose down
docker-compose up -d
```

Wait a few seconds for the backend to start.

---

## Step 5: Test OAuth Login

### 5.1 Open GitPeek

Open your browser to: http://localhost:3000

### 5.2 Click "Login with GitHub"

Click the blue **"Login with GitHub"** button in the top right corner.

### 5.3 Authorize the Application

You'll be redirected to GitHub's website. You should see:
```
Authorize GitPeek
GitPeek by [your-username] would like permission to:
☑ Read and write access to your repositories
☑ Read access to your profile
```

Click **"Authorize [your-username]"**

### 5.4 Success!

You'll be redirected back to GitPeek and:
- ✅ You'll see your username in the top right
- ✅ You'll see your avatar
- ✅ You're now logged in!

---

## Step 6: View Your Private Repositories

### 6.1 Search for Yourself

In the search box, enter your GitHub username and click **Search**.

### 6.2 See the Magic! ✨

You should now see:
- ✅ All your public repositories
- ✅ All your private repositories (marked with "Private" badge)
- ✅ Commits to private repos
- ✅ Complete activity from private projects

---

## 🔧 Troubleshooting

### Problem: "404 Page Not Found" After Clicking Login

**Cause:** Callback URL mismatch

**Solution:**
1. Go back to https://github.com/settings/developers
2. Click on your GitPeek OAuth app
3. Make sure **Authorization callback URL** is exactly: `http://localhost:3000/auth/callback`
4. Click **Update application**
5. Try logging in again

### Problem: Login Button Does Nothing

**Cause:** Backend doesn't have OAuth credentials

**Solution:**
1. Check that `.env` file exists in the GitPeek root directory
2. Check that it has your Client ID and Client Secret
3. Restart backend: `docker-compose restart backend`
4. Check backend logs: `docker-compose logs backend`

### Problem: "Invalid Client" Error on GitHub

**Cause:** Wrong Client ID or Client Secret

**Solution:**
1. Double-check your `.env` file
2. Make sure there are no extra spaces
3. Make sure you copied the full Client ID and Secret
4. Restart backend: `docker-compose restart backend`

### Problem: Can't See Private Repos After Login

**Cause:** Not searching for yourself or authorized user

**Solution:**
- Make sure you're searching for YOUR GitHub username
- Private repos only show if you own them or have access
- Log out and log back in to refresh permissions

### Problem: Backend Won't Start After Adding Credentials

**Cause:** Syntax error in `.env` file

**Solution:**
```bash
# Check backend logs
docker-compose logs backend

# Common issues:
# - Missing quotes around values (not needed)
# - Extra spaces
# - Missing equals sign
# - Wrong line endings (Windows vs Linux)

# Correct format (no quotes needed):
GITHUB_CLIENT_ID=abc123
GITHUB_CLIENT_SECRET=xyz789
```

---

## 🔄 For Production Deployment

If you're deploying GitPeek to a public URL (like Vercel/Render):

### 1. Create a New OAuth App for Production

Go to https://github.com/settings/developers and create a **second** OAuth app:

```
Application name: GitPeek Production
Homepage URL: https://your-domain.com
Authorization callback URL: https://your-domain.com/auth/callback
```

⚠️ Use your actual production domain!

### 2. Add Credentials to Hosting Platform

**For Render (Backend):**
1. Go to your Render dashboard
2. Select your service
3. Go to "Environment"
4. Add variables:
   - `GITHUB_CLIENT_ID`: [production client id]
   - `GITHUB_CLIENT_SECRET`: [production client secret]
   - `GITHUB_REDIRECT_URI`: `https://your-frontend.com/auth/callback`

**For Vercel (Frontend):**
Frontend doesn't need credentials - they're only on the backend!

### 3. Redeploy

Redeploy both frontend and backend to pick up the new configuration.

---

## 🛡️ Security Best Practices

### ✅ DO:
- ✅ Keep your Client Secret **SECRET**
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Create separate OAuth apps for development and production
- ✅ Regenerate secrets if they're ever exposed
- ✅ Review authorized applications periodically

### ❌ DON'T:
- ❌ Commit `.env` to git
- ❌ Share your Client Secret with anyone
- ❌ Use production credentials for development
- ❌ Post your credentials in Discord/Slack/etc.
- ❌ Include credentials in screenshots

---

## 🔐 Revoking Access

### To Revoke a User's Access

Users can revoke GitPeek's access anytime:
1. Go to https://github.com/settings/applications
2. Find "GitPeek" under "Authorized OAuth Apps"
3. Click **Revoke**

### To Delete Your OAuth App

If you want to delete the OAuth app entirely:
1. Go to https://github.com/settings/developers
2. Click on your GitPeek OAuth app
3. Scroll to bottom
4. Click **Delete application**
5. Confirm deletion

---

## ❓ FAQ

### Q: Do I need to create an OAuth app for each user?

**A:** No! Each user who wants OAuth access creates their **own** OAuth app with **their own** credentials. You don't share credentials.

### Q: Can I use GitPeek without OAuth?

**A:** Yes! GitPeek works perfectly for viewing public repositories without any OAuth setup.

### Q: What permissions does GitPeek request?

**A:** GitPeek requests:
- `repo` - To read your repositories (public and private)
- `user` - To read your basic profile information

These are read-only permissions. GitPeek cannot modify or delete your repositories.

### Q: Is my Client Secret safe?

**A:** Yes, if you:
1. Keep it in `.env` (which is not committed to git)
2. Only use it in the backend (never frontend)
3. Don't share it with others

The `.env` file is already in `.gitignore`, so it won't be committed.

### Q: Can someone steal my Client Secret?

**A:** Not if you follow best practices:
- ✅ `.env` is not committed to git
- ✅ Secret is only in backend container
- ✅ Backend runs on your machine or secure server
- ✅ Secret is never sent to frontend or users

### Q: What happens if my secret is exposed?

**A:**
1. Go to https://github.com/settings/developers
2. Click on your OAuth app
3. Click **"Regenerate secret"**
4. Update your `.env` file
5. Restart backend

### Q: How many users can use my OAuth app?

**A:** Technically unlimited, but:
- Each OAuth app has rate limits (5000 requests/hour)
- For personal use, create your own OAuth app
- For shared deployment, one OAuth app can serve all users

### Q: Do users see my OAuth credentials?

**A:** No! Users only:
- Click "Login with GitHub"
- Enter their own GitHub username/password on GitHub's site
- Authorize your app
- Never see your Client ID or Secret

---

## 📚 Additional Resources

- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [OAuth 2.0 Explained](https://www.oauth.com/)

---

## 🆘 Still Having Issues?

If you're still having trouble:

1. **Check the logs:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Verify your setup:**
   ```bash
   # Check .env exists
   ls -la .env

   # Restart everything
   docker-compose down
   docker-compose up -d

   # Check containers are running
   docker-compose ps
   ```

3. **Open an issue:**
   - Go to the GitHub repository
   - Click "Issues"
   - Describe your problem
   - Include relevant logs (without credentials!)

---

**🎉 Congratulations!** If you made it this far, you should now have OAuth working and be able to view your private repositories!

Remember: **OAuth is optional** - GitPeek works great without it for public repos!

