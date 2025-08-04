# How to Upload ShadowLure to GitHub

This guide provides the exact commands to upload your project to a new GitHub repository.

---

### Step 1: Create a New Repository on GitHub

1.  Go to [GitHub.com](https://github.com) and log in.
2.  Click the **`+`** icon in the top-right corner and select **"New repository"**.
3.  **Repository name:** `ShadowLure`
4.  **Description:** `A simple and extensible honeypot framework in Python.`
5.  Select **Public**.
6.  **IMPORTANT:** Leave all the "Initialize this repository with" options **unchecked**.
7.  Click **"Create repository"**.

---

### Step 2: Run These Commands in Your Project Terminal

After creating the repository, GitHub will show you a page with commands. The commands below are tailored for your project.

Open a terminal in your project's directory (`c:/Users/Windroxd/Documents/HoneyPotInter`) and run these commands one by one.

1.  **Initialize Git:**
    This turns your project folder into a Git repository.
    ```bash
    git init
    ```

2.  **Add All Files:**
    This prepares all your project files to be saved.
    ```bash
    git add .
    ```

3.  **Create the First Save (Commit):**
    This creates the first version of your project.
    ```bash
    git commit -m "Initial commit: Create ShadowLure honeypot framework"
    ```

4.  **Set the Main Branch Name:**
    This is the standard name for the primary branch.
    ```bash
    git branch -M main
    ```

5.  **Link Your Project to GitHub:**
    This tells Git where to upload your files. **Replace `YOUR_USERNAME` with your actual GitHub username.**
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/ShadowLure.git
    ```

6.  **Upload Your Project:**
    This pushes all your files to GitHub.
    ```bash
    git push -u origin main
    ```

---

After running these commands, refresh your GitHub repository page. You will see all your project files, including the professional `README.md`, ready to be shared.
