[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/15.0)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

## Application of a Product Processing Company

Develop an application for a product processing company to streamline and optimize operational processes, from the acquisition of raw materials to the delivery of the finished product.

## Description

Our application is designed to manage every aspect of our food processing operations. Key features include inventory management, production scheduling, quality control tracking, and regulatory compliance. By automating these processes, we aim to increase efficiency, reduce food waste, and ensure the highest quality products for our customers.

## Index

* [Characteristics](#characteristics)
* [Project Architecture](#project-architecture)
* [Tools](#tools)
* [Screenshots](#screenshots)

## Characteristics

* Manage basic information of a company.
* Manage merchandise information.
* Manage the warehouses that the company owns.
* Manage the areas that a warehouse has.
* Manage basic customer information.
* Manage the mobilization guides that an invoice has.
* Allow the movement of goods from a port to a warehouse area
* Allow the movement of merchandise from one area of ​​a warehouse to another different area
* Create invoices for the transfer of purchased merchandise.
* Create invoices for payments of merchandise made by a customer.
* Allow payment of a payment invoice.
* Allow the preparation of reports on payment invoices and the transfer of goods.

## Project Architecture

Odoo consists of a three-tier architecture. This architecture divides the application into the following tiers (see figure below):

* The presentation tier, consisting of a user interface (UI) on the web.
* The application tier, where logic of the application resides.
* The data tier, where data is stored and managed.

The database tier stores all information and configurations of the Odoo modules. Meanwhile, on the application tier resides the Odoo server. This server stores application logic, handles communication between different modules, and provides the Object Relational Mapping (ORM) tool to transfer data from the Odoo server in Python to a PostgreSQL database server. The highest tier, which is written in Javascript, is the presentation tier (UI in a web browser).

![Imagen de diagrama de capas](/media/images/3-tier-architecture.png)

## Tools

The following tools were used to develop the system:

* **Odoo**: It is a highly customizable open source enterprise application platform, and Python is the programming language that powers its development. This respects the design pattern known as model-view-controller.

* **CSS**: It is a fundamental tool to customize and stylize the user interface in Odoo.

* **DataBase**: The database used is postgreSQL managed through the Odoo ORM.

## Screenshots

In order to use the application you must look for the custom-addons folder and inside it we place procesadora_productos. folder.

### **View Companies**

![View Companies](/media/images/view_companies.png)

### **Create Company**

![Create Company](/media/images/create_company.png)

### **View Merchandise**

![View merchandise](/media/images/view_merchandise.png)


### **Create Transfer Invoice**

![Create transfer invoice](/media/images/create_transfer_invoice.png)


### **Create Port Mobilization Request**

![Create Port Mobilization Request](/media/images/create_port_mobilization_request.png)

### **Create a Payment Note**

![Create a Payment Note](/media/images/create_payment_note.png)

Odoo
----

Odoo is a suite of web based open source business apps.

The main Odoo Apps include an <a href="https://www.odoo.com/page/crm">Open Source CRM</a>,
<a href="https://www.odoo.com/app/website">Website Builder</a>,
<a href="https://www.odoo.com/app/ecommerce">eCommerce</a>,
<a href="https://www.odoo.com/app/inventory">Warehouse Management</a>,
<a href="https://www.odoo.com/app/project">Project Management</a>,
<a href="https://www.odoo.com/app/accounting">Billing &amp; Accounting</a>,
<a href="https://www.odoo.com/app/point-of-sale-shop">Point of Sale</a>,
<a href="https://www.odoo.com/app/employees">Human Resources</a>,
<a href="https://www.odoo.com/app/social-marketing">Marketing</a>,
<a href="https://www.odoo.com/app/manufacturing">Manufacturing</a>,
<a href="https://www.odoo.com/">...</a>

Odoo Apps can be used as stand-alone applications, but they also integrate seamlessly so you get
a full-featured <a href="https://www.odoo.com">Open Source ERP</a> when you install several Apps.

Getting started with Odoo
-------------------------

For a standard installation please follow the <a href="https://www.odoo.com/documentation/15.0/administration/install.html">Setup instructions</a>
from the documentation.

To learn the software, we recommend the <a href="https://www.odoo.com/slides">Odoo eLearning</a>, or <a href="https://www.odoo.com/page/scale-up-business-game">Scale-up</a>, the <a href="https://www.odoo.com/page/scale-up-business-game">business game</a>. Developers can start with <a href="https://www.odoo.com/documentation/15.0/developer/howtos.html">the developer tutorials</a>
