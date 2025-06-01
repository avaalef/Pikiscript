import requests
import argparse

class PikiScriptEngine:
    def __init__(self, username, option):
        self.username = username
        self.option = option
        self.posts_url = f"https://pikidiary-api.vercel.app?username={username}&show=posts"
        self.achievements_url = f"https://pikidiary-api.vercel.app?username={username}&show=achievements"
        self.badges_url = f"https://pikidiary-api.vercel.app?username={username}&show=badges"
        self.posts = []
        self.achievements = []
        self.badges = []

    def fetch_posts(self):
        response = requests.get(self.posts_url)
        if response.status_code == 200:
            data = response.json()
            self.posts = data.get("posts", [])
        else:
            print(f"Error fetching posts: {response.status_code}")

    def fetch_achievements(self):
        response = requests.get(self.achievements_url)
        if response.status_code == 200:
            data = response.json()
            self.achievements = data.get("achievements", [])
        else:
            print(f"Error fetching achievements: {response.status_code}")

    def fetch_badges(self):
        response = requests.get(self.badges_url)
        if response.status_code == 200:
            data = response.json()
            self.badges = data.get("badges", [])
        else:
            print(f"Error fetching badges: {response.status_code}")

    def print_post(self, post):
        print(f"— @{post['author']} posted at {post['createdAt']}:")
        print(f'   "{post["content"]}"')
        if post.get("isReply", False):
            print("   This post is a reply.")
        if post.get("media", []):
            print("   Includes image.")
        print(f"   Likes: {post.get('likes', 0)}")
        print(f"   URL: {post['url']}")
        print("-----------------------------")

    def print_achievements(self):
        if not self.achievements:
            print("No achievements found.")
            return
        print("Achievements:")
        for ach in self.achievements:
            print(f" - {ach}")

    def print_badges(self):
        if not self.badges:
            print("No badges found.")
            return
        print("Badges:")
        for badge in self.badges:
            print(f" - {badge}")

    def run(self):
        if self.option in ["posts", "everything"]:
            self.fetch_posts()
            if not self.posts:
                print("No posts found.")
            else:
                for post in self.posts:
                    self.print_post(post)

        if self.option in ["achievements", "everything"]:
            self.fetch_achievements()
            self.print_achievements()

        if self.option in ["badges", "everything"]:
            self.fetch_badges()
            self.print_badges()

def choose_option():
    print("What do you want to see?")
    print("(1) Show Achievements Only")
    print("(2) Show Badges Only")
    print("(3) Show Posts Only")
    print("(4) Show All")
    choice = input("Enter option (1-4): ").strip()
    mapping = {
        "1": "achievements",
        "2": "badges",
        "3": "posts",
        "4": "everything"
    }
    return mapping.get(choice, "posts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username', nargs='?', help='Username to fetch data for')
    parser.add_argument('--option', choices=['posts', 'achievements', 'badges', 'everything'], default=None)

    args = parser.parse_args()

    if not args.username:
        args.username = input("Enter username: ").strip()
        if not args.username:
            print("Username is required.")
            exit(1)

    option = args.option
    if not option:
        option = choose_option()

    engine = PikiScriptEngine(args.username, option)
    engine.run()

    input("Press ENTER to exit...")
