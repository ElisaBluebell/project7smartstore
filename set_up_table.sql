-- 스키마 제작
CREATE SCHEMA `project7smartstore`;
-- 회원 가입을 통해 받는 유저 정보 테이블
CREATE TABLE `project7smartstore`.`user_info` (`user_idx` INT NOT NULL AUTO_INCREMENT, `user_id` VARCHAR(16) NOT NULL, `user_pw` VARCHAR(16) NOT NULL, `user_name` VARCHAR(16) NOT NULL, `user_tel` INT NOT NULL, `temp` VARCHAR(16), `user_type` INT NOT NULL, PRIMARY KEY(idx));
-- 상품 정보 테이블
CREATE TABLE `project7smartstore`.`product_info` (`product_idx` INT NOT NULL AUTO_INCREMENT, `product_name` VARCHAR(16) NOT NULL, `temp` BLOB, PRIMARY KEY(`product_idx`));
-- 주문 관리
CREATE TABLE `project7smartstore`.`order_management` (`order_idx` INT NOT NULL AUTO_INCREMENT, `product_idx` INT NOT NULL, `product_name` VARCHAR(16) NOT NULL, `product_quantity` INT NOT NULL, `customer_idx` INT NOT NULL, `customer_name` VARCHAR(16) NOT NULL, PRIMARY KEY(`order_idx`));
-- BoM
CREATE TABlE `project7smartstore`.`bill_of_material` (`recipe_idx` INT NOT NULL AUTO_INCREMENT, `product_idx` INT NOT NULL, `product_name` VARCHAR(16) NOT NULL, `material_idx` INT NOT NULL, `material_name` VARCHAR(16) NOT NULL, `material_quantity` INT NOT NULL, `measure_unit` VARCHAR(5), PRIMARY KEY(`recipe_idx`));
-- 재고 관리
CREATE TABLE `project7smartstore`.`material_management` (`material_idx` INT NOT NULL AUTO_INCREMENT, `material_name` VARCHAR(16) NOT NULL, `inventory_quantity` INT NOT NULL, PRIMARY KEY(`material_idx`));
-- 문의 관리
CREATE TABLE `project7smartstore`.`faq_management` (`faq_idx` INT NOT NULL AUTO_INCREMENT, `seller_idx` INT NOT NULL, `seller_name` VARCHAR(16) NOT NULL, `buyer_idx` INT NOT NULL, `buyer_name` VARCHAR(16) NOT NULL, `product_idx` INT NOT NULL, `product_name` VARCHAR(16) NOT NULL, `faq_type` INT NOT NULL, `faq_content` VARCHAR(200) NOT NULL, `faq_process` INT NOT NULL, PRIMARY KEY(`faq_idx`));