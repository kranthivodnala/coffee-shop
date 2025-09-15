# coffee-shop
Sample Coffee Shop Python Application

## Requirements

- AWS Account (You can create a free account)
- EC2 Instance (to host the application)
- Key Pair (to connect to the EC2)
- Security Groups (allow application to connect)
- SQLite is used as the database engine (stores all data in a single file on disk)

## Steps to Host the coffee-shop Application

1. **Login to AWS Account**
2. **Navigate to nearest availability zone**
3. **Launch EC2 Instance**
    - Select Amazon Linux AMI
    - Select `t3.micro`
    - Create a new security group allowing SSH from your IP and open port 80
4. **Login to EC2 Instance**
5. **Run the following commands to update, install git, and docker**  
    ```sh
    sudo su -
    yum update -y
    yum install git -y
    yum install docker -y
    ```
6. **Clone the GitHub repo**
7. **Navigate to the coffee-shop directory**
8. **Build the Docker image**
    ```sh
    docker build -t coffeeshop:latest .
    ```
9. **Check built Docker images**
    ```sh
    docker images
    ```
10. **Run the Docker container**
    ```sh
    docker run -d --restart unless-stopped -p 80:8000 -v /srv/coffee-data:/data --name coffeeshop coffeeshop:latest
    ```
11. **Check running Docker containers**
    ```sh
    docker ps -a
    ```
12. **Access the website**
    - Open your EC2 Public IP address in a browser
13. **Enter a couple of orders**

## Validations

Once orders are placed, use the following commands to check the menu and orders:

- **List menu items**
    ```sh
    curl http://<EC2_PUBLIC_IP>/api/menu
    ```
- **List all orders**
    ```sh
    curl http://<EC2_PUBLIC_IP>/api/orders
    ```

- **Login to DB to check the orders are created**
    ```sh
    sudo yum install -y sqlite3
    sqlite3 /srv/coffee-data/coffee_shop.db "SELECT * FROM orders;"
    ```