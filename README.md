
# **Setting Up a Secure Mail Server with Docker Mailserver**

In today's digital world, managing a reliable and secure mail server is crucial for any organization. With the rise of containerization technologies like Docker, setting up and managing a mail server has become more accessible and streamlined. In this article, we will walk through the process of setting up a mail server using Docker Mailserver, covering prerequisites, installation, configuration, and best practices to ensure a secure and efficient email system.

## **Introduction**

Docker Mailserver is a popular open-source mail server suite that simplifies the deployment and management of a mail server using Docker containers. It provides an all-in-one solution for handling SMTP, IMAP, and POP3 services, along with support for security features such as DKIM, SPF, and DMARC. This article will guide you through the complete setup of Docker Mailserver, from initial installation to fine-tuning your server for optimal performance and security.

---

## **Prerequisites**

Before diving into the setup process, ensure you have the following prerequisites:

- **Mail Domain Name**: A registered domain name for your mail server (e.g., `mail.example.com`).
- **Docker and Docker Compose**: Installed on your server.

---

## **Setup**

### **1. Create Docker Compose File**

Create a `docker-compose.yml` file with the following content to define the mail server service:

```yaml
version: "3"

networks:
  mailserver:
    name: mailserver

services:
  mailserver:
    image: docker.io/mailserver/docker-mailserver:13.0.1
    container_name: mail.example.com
    hostname: mail.example.com
    env_file: mailserver.env
    ports:
      - "25:25"    # SMTP
      - "143:143"  # IMAP4
      - "465:465"  # ESMTP
      - "587:587"  # ESMTP
      - "993:993"  # IMAP4
    volumes:
      - ./docker-data/dms/mail-data/:/var/mail/
      - ./docker-data/dms/mail-state/:/var/mail-state/
      - ./docker-data/dms/mail-logs/:/var/log/mail/
      - ./docker-data/dms/config/:/tmp/docker-mailserver/
      - /etc/localtime:/etc/localtime:ro
      - /home/docker-user/traefik/acme.json:/etc/letsencrypt/acme.json:ro
    restart: always
    stop_grace_period: 1m
    cap_add:
      - NET_ADMIN
    healthcheck:
      test: "ss --listening --tcp | grep -P 'LISTEN.+:smtp' || exit 1"
      timeout: 3s
      retries: 5
    networks:
      - mailserver
```

### **2. Environment File**

Adjust any of the environment variables to better fit your configuration and needs.

### **3. Create Directories**

Create the necessary directories for storing mail data, state, logs, and configuration:

```bash
mkdir -p docker-data/dms/mail-data
mkdir -p docker-data/dms/mail-state
mkdir -p docker-data/dms/mail-logs
mkdir -p docker-data/dms/config
```

### **4. Run Docker Compose**

Start the mail server container:

```bash
docker-compose up -d
```

### **5. Create Email Address**

Add an email address using the provided `setup.sh` script:

```bash
./setup.sh email add admin@mail.example.com
```

### **6. Configure DKIM**

Generate DKIM keys and configure your DNS:

```bash
./setup.sh config dkim
```

Add the DKIM TXT record to your DNS settings based on the output file located at `./docker-data/dms/config/opendkim/keys/mail.example.com/mail.txt`.

### **7. Restart the Container**

After configuring DKIM and SPF records, restart the container to apply changes:

```bash
docker-compose restart
```

---

## DNS Records

### 1. **MX Record**
- **Name**: @
- **Type**: MX
- **Value**: `mail.example.com`
- **Priority**: 1

### 2. **DKIM Record**
- **Name**: `mail._domainkey.mail`
- **Type**: TXT
- **Value**: 
  ```
  v=DKIM1; h=sha256; k=rsa; p=MIIBIRANDOMudT8ywZatm/vF1Bofy3A+5iPhiIPJFmztU5mQuWcnu4Ml5WYQRP3UFyRANDOMUxNwqZfHsZ+Xl+uac+6AeUduDtRQSxtpDauNM4X/f7sGPlu3ExtoRANDOMrmVAM5NIPrjD1dhUcEYKaaCtbZ+OxZ688lsECgHa7dk1Zchv+8RpKO2nRvB2pUg/5Cls9eATVkkHh4qY0/cWPt8PmaBEtANgAPXeJxDz3Q/X4vS5W+2hsRANDOMcBxGBfo7VPLAnL87GDzG3HUONSYn0Ct6YJRANDOMAlYswiSuZQwIDAQAB
  ```
  Use the generated DKIM key

### 3. **SPF Record**
- **Name**: @
- **Type**: TXT
- **Value**: 
  ```
  v=spf1 mx a:mail.example.com include:mail.example.com +all
  ```

### 4. **DMARC Record** (for completeness)
- **Name**: `_dmarc`
- **Type**: TXT
- **Value**: 
  ```
  v=DMARC1; p=none; rua=mailto:admin@mail.example.com; ruf=mailto:admin@mail.example.com; sp=none; ri=86400
  ```

---

## **Testing and Troubleshooting**

### Postfix Email Reception Troubleshooting Guide

If you are experiencing issues with receiving emails, follow these detailed guidelines to troubleshoot and resolve the problem:

#### 1. **Verify Configuration**

- **Check Configuration Files:**
  - Ensure the `myhostname` and `mydomain` variables are correctly set.
  - Refer to the provided `utils/postfix.conf.example` for configuration details. Check the `IMPORTANT` section. Verify that these values are correctly set in the `/etc/postfix/main.cf` file.
	  ```conf
	  mydestination = localhost.$mydomain, localhost
	  myhostname = mail.bansira.com
	  mydomain = mail.bansira.com
	  ```

- **Apply Changes:**
  - Reload Postfix to apply if there are any changes in the config file.
    ```bash
    postfix reload
    ```

#### 2. **Check Logs**

- **Review Logs:**
  - Examine Postfix logs for any errors or warnings that might indicate configuration issues or other problems.

#### 3. **Network and Firewall**

- **Check Port Accessibility:**
  - Ensure that necessary ports (e.g., 25 for SMTP, 587 for submission) are open and not blocked by firewalls.

#### 4. **Testing**

- **Verify Connectivity:**
  - Use tools like `telnet` or `nc` to test connectivity to the mail server.

#### 5. **Additional Tips**

- For further assistance, consult the [Postfix documentation](http://www.postfix.org/documentation.html) or relevant community forums.

### **1. Email Delivery Testing**

Use online tools to test the configuration of your mail server. Some useful tools include:

- [Mail Tester](https://www.mail-tester.com/)
- [MxToolbox](https://mxtoolbox.com/)

### **2. Logs and Debugging**

Monitor the logs to troubleshoot issues:

```bash
docker-compose logs -f
```

Check logs located in `docker-data/dms/mail-logs/` for detailed information.

### **3. Verify DNS Records**

Ensure that DKIM, SPF, and MX records are correctly configured using tools like:

- [DNS Checker](https://dnschecker.org/)
- [MXToolbox SPF Check](https://mxtoolbox.com/spf.aspx)

---

## **Useful Links and Resources**

1. [Docker Mailserver GitHub Repository](https://github.com/docker-mailserver/docker-mailserver)
2. [Official Postfix Documentation](http://www.postfix.org/documentation.html)
3. [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---