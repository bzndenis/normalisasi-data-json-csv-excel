/*
 Navicat Premium Dump SQL

 Source Server         : Local Postgre
 Source Server Type    : PostgreSQL
 Source Server Version : 140005 (140005)
 Source Host           : localhost:5432
 Source Catalog        : gokendali_dev
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140005 (140005)
 File Encoding         : 65001

 Date: 13/01/2026 00:16:42
*/


-- ----------------------------
-- Type structure for BeritaStatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."BeritaStatus";
CREATE TYPE "public"."BeritaStatus" AS ENUM (
  'pending',
  'approved',
  'rejected'
);

-- ----------------------------
-- Type structure for SettingCategory
-- ----------------------------
DROP TYPE IF EXISTS "public"."SettingCategory";
CREATE TYPE "public"."SettingCategory" AS ENUM (
  'general',
  'email',
  'system',
  'security',
  'notification'
);

-- ----------------------------
-- Type structure for SettingType
-- ----------------------------
DROP TYPE IF EXISTS "public"."SettingType";
CREATE TYPE "public"."SettingType" AS ENUM (
  'string',
  'number',
  'boolean',
  'json'
);

-- ----------------------------
-- Type structure for UserType
-- ----------------------------
DROP TYPE IF EXISTS "public"."UserType";
CREATE TYPE "public"."UserType" AS ENUM (
  'admin',
  'petugas',
  'user',
  'pendamping'
);

-- ----------------------------
-- Sequence structure for apresiasi_apresiasi_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."apresiasi_apresiasi_id_seq";
CREATE SEQUENCE "public"."apresiasi_apresiasi_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for apresiasi_pemda_apresiasi_pemda_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."apresiasi_pemda_apresiasi_pemda_id_seq";
CREATE SEQUENCE "public"."apresiasi_pemda_apresiasi_pemda_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for apresiasi_pemda_detail_detail_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."apresiasi_pemda_detail_detail_id_seq";
CREATE SEQUENCE "public"."apresiasi_pemda_detail_detail_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for arsip_arsip_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."arsip_arsip_id_seq";
CREATE SEQUENCE "public"."arsip_arsip_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for banners_banner_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."banners_banner_id_seq";
CREATE SEQUENCE "public"."banners_banner_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for berita_berita_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."berita_berita_id_seq";
CREATE SEQUENCE "public"."berita_berita_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for buku_buku_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."buku_buku_id_seq";
CREATE SEQUENCE "public"."buku_buku_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for evaluasi_detail_detail_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."evaluasi_detail_detail_id_seq";
CREATE SEQUENCE "public"."evaluasi_detail_detail_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for evaluasi_evaluasi_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."evaluasi_evaluasi_id_seq";
CREATE SEQUENCE "public"."evaluasi_evaluasi_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for kategori_kategori_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."kategori_kategori_id_seq";
CREATE SEQUENCE "public"."kategori_kategori_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for kinerja_kps_kinerja_kps_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."kinerja_kps_kinerja_kps_id_seq";
CREATE SEQUENCE "public"."kinerja_kps_kinerja_kps_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_apresiasi_pemda_kriteria_kriteria_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_apresiasi_pemda_kriteria_kriteria_id_seq";
CREATE SEQUENCE "public"."master_apresiasi_pemda_kriteria_kriteria_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_bps_bps_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_bps_bps_id_seq";
CREATE SEQUENCE "public"."master_bps_bps_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kategori_lampiran_pengawasan_kategori_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kategori_lampiran_pengawasan_kategori_id_seq";
CREATE SEQUENCE "public"."master_kategori_lampiran_pengawasan_kategori_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kategori_sertifikat_kategori_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kategori_sertifikat_kategori_id_seq";
CREATE SEQUENCE "public"."master_kategori_sertifikat_kategori_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kps_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kps_id_seq";
CREATE SEQUENCE "public"."master_kps_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kriteria_kategori_kategori_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kriteria_kategori_kategori_id_seq";
CREATE SEQUENCE "public"."master_kriteria_kategori_kategori_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kriteria_kriteria_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kriteria_kriteria_id_seq";
CREATE SEQUENCE "public"."master_kriteria_kriteria_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kriteria_tipe_tipe_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kriteria_tipe_tipe_id_seq";
CREATE SEQUENCE "public"."master_kriteria_tipe_tipe_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_kups_kups_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_kups_kups_id_seq";
CREATE SEQUENCE "public"."master_kups_kups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_pemda_pemda_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_pemda_pemda_id_seq";
CREATE SEQUENCE "public"."master_pemda_pemda_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for master_pendamping_pendamping_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."master_pendamping_pendamping_id_seq";
CREATE SEQUENCE "public"."master_pendamping_pendamping_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for pemantauan_pemantauan_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pemantauan_pemantauan_id_seq";
CREATE SEQUENCE "public"."pemantauan_pemantauan_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for pendampingan_pendampingan_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pendampingan_pendampingan_id_seq";
CREATE SEQUENCE "public"."pendampingan_pendampingan_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for pengawasan_pengawasan_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pengawasan_pengawasan_id_seq";
CREATE SEQUENCE "public"."pengawasan_pengawasan_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for permissions_permission_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."permissions_permission_id_seq";
CREATE SEQUENCE "public"."permissions_permission_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for pesan_kps_pesan_kps_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."pesan_kps_pesan_kps_id_seq";
CREATE SEQUENCE "public"."pesan_kps_pesan_kps_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for publikasi_publikasi_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."publikasi_publikasi_id_seq";
CREATE SEQUENCE "public"."publikasi_publikasi_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for riwayat_riwayat_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."riwayat_riwayat_id_seq";
CREATE SEQUENCE "public"."riwayat_riwayat_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for role_permissions_role_permission_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."role_permissions_role_permission_id_seq";
CREATE SEQUENCE "public"."role_permissions_role_permission_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for roles_role_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."roles_role_id_seq";
CREATE SEQUENCE "public"."roles_role_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for sertifikat_pendamping_sertifikat_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."sertifikat_pendamping_sertifikat_id_seq";
CREATE SEQUENCE "public"."sertifikat_pendamping_sertifikat_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for settings_setting_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."settings_setting_id_seq";
CREATE SEQUENCE "public"."settings_setting_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for user_roles_user_role_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."user_roles_user_role_id_seq";
CREATE SEQUENCE "public"."user_roles_user_role_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_user_id_seq";
CREATE SEQUENCE "public"."users_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for _prisma_migrations
-- ----------------------------
DROP TABLE IF EXISTS "public"."_prisma_migrations";
CREATE TABLE "public"."_prisma_migrations" (
  "id" varchar(36) COLLATE "pg_catalog"."default" NOT NULL,
  "checksum" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "finished_at" timestamptz(6),
  "migration_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "logs" text COLLATE "pg_catalog"."default",
  "rolled_back_at" timestamptz(6),
  "started_at" timestamptz(6) NOT NULL DEFAULT now(),
  "applied_steps_count" int4 NOT NULL DEFAULT 0
)
;

-- ----------------------------
-- Table structure for apresiasi
-- ----------------------------
DROP TABLE IF EXISTS "public"."apresiasi";
CREATE TABLE "public"."apresiasi" (
  "apresiasi_id" int4 NOT NULL DEFAULT nextval('apresiasi_apresiasi_id_seq'::regclass),
  "apresiasi_pendamping" int4,
  "apresiasi_waktu_upload" timestamp(6),
  "apresiasi_alasan" varchar(1000) COLLATE "pg_catalog"."default",
  "apresiasi_rkps" int4,
  "apresiasi_rkt" int4,
  "apresiasi_adrt" int4,
  "apresiasi_koperasi" int4,
  "apresiasi_andil" int4,
  "apresiasi_batas" int4,
  "apresiasi_legal" int4,
  "apresiasi_sertifikasi" int4,
  "apresiasi_sni" int4,
  "apresiasi_kerjasama" int4,
  "apresiasi_keberlanjutan" varchar(1000) COLLATE "pg_catalog"."default",
  "apresiasi_daya" varchar(1000) COLLATE "pg_catalog"."default",
  "apresiasi_regenerasi" varchar(1000) COLLATE "pg_catalog"."default",
  "apresiasi_inovasi" varchar(1000) COLLATE "pg_catalog"."default",
  "apresiasi_petugas" int4
)
;

-- ----------------------------
-- Table structure for apresiasi_pemda
-- ----------------------------
DROP TABLE IF EXISTS "public"."apresiasi_pemda";
CREATE TABLE "public"."apresiasi_pemda" (
  "apresiasi_pemda_id" int4 NOT NULL DEFAULT nextval('apresiasi_pemda_apresiasi_pemda_id_seq'::regclass),
  "pemda_id" int4 NOT NULL,
  "tahun" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "tanggal_penilaian" date NOT NULL,
  "versi_kriteria" int4 NOT NULL,
  "total_nilai" numeric(10,2) NOT NULL,
  "apresiasi_petugas" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for apresiasi_pemda_detail
-- ----------------------------
DROP TABLE IF EXISTS "public"."apresiasi_pemda_detail";
CREATE TABLE "public"."apresiasi_pemda_detail" (
  "detail_id" int4 NOT NULL DEFAULT nextval('apresiasi_pemda_detail_detail_id_seq'::regclass),
  "apresiasi_pemda_id" int4 NOT NULL,
  "kriteria_id" int4 NOT NULL,
  "kriteria_versi" int4 NOT NULL,
  "jawaban" bool NOT NULL,
  "nilai" numeric(10,2) NOT NULL,
  "bobot_saat_penilaian" numeric(5,2) NOT NULL,
  "deskripsi" text COLLATE "pg_catalog"."default",
  "file_attachment" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for arsip
-- ----------------------------
DROP TABLE IF EXISTS "public"."arsip";
CREATE TABLE "public"."arsip" (
  "arsip_id" int4 NOT NULL DEFAULT nextval('arsip_arsip_id_seq'::regclass),
  "arsip_waktu_upload" timestamp(6) NOT NULL,
  "arsip_petugas" int4 NOT NULL,
  "arsip_kode" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "arsip_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "arsip_pendidikan" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "arsip_jk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "arsip_kategori" int4 NOT NULL,
  "arsip_pekerjaan" varchar(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT ''::character varying,
  "arsip_file" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "arsip_foto" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for arsip1
-- ----------------------------
DROP TABLE IF EXISTS "public"."arsip1";
CREATE TABLE "public"."arsip1" (
  "arsip1_id" int4,
  "arsip1_waktu_upload" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_kode" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_nama" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_kategori" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_jenis" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_petugas" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_keterangan" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_jk" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_file" varchar(512) COLLATE "pg_catalog"."default",
  "arsip1_foto" varchar(512) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for banners
-- ----------------------------
DROP TABLE IF EXISTS "public"."banners";
CREATE TABLE "public"."banners" (
  "banner_id" int4 NOT NULL DEFAULT nextval('banners_banner_id_seq'::regclass),
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "tanggal" timestamp(6) NOT NULL,
  "banner_url" text COLLATE "pg_catalog"."default",
  "is_active" bool NOT NULL DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for berita
-- ----------------------------
DROP TABLE IF EXISTS "public"."berita";
CREATE TABLE "public"."berita" (
  "berita_id" int4 NOT NULL DEFAULT nextval('berita_berita_id_seq'::regclass),
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "tanggal" timestamp(6) NOT NULL,
  "thumbnail_url" text COLLATE "pg_catalog"."default",
  "banner_url" text COLLATE "pg_catalog"."default",
  "tampilkan_ke" int4,
  "is_active" bool NOT NULL DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "status" "public"."BeritaStatus" NOT NULL DEFAULT 'pending'::"BeritaStatus",
  "user_id" int4,
  "published_admin_id" int4,
  "slug" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for buku
-- ----------------------------
DROP TABLE IF EXISTS "public"."buku";
CREATE TABLE "public"."buku" (
  "buku_id" int4 NOT NULL DEFAULT nextval('buku_buku_id_seq'::regclass),
  "judul_utama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "judul_lengkap" text COLLATE "pg_catalog"."default" NOT NULL,
  "detail_tambahan" text COLLATE "pg_catalog"."default",
  "kategori" varchar(100) COLLATE "pg_catalog"."default",
  "tahun" varchar(50) COLLATE "pg_catalog"."default",
  "thumbnail_url" text COLLATE "pg_catalog"."default",
  "file_url" text COLLATE "pg_catalog"."default",
  "is_active" bool NOT NULL DEFAULT true,
  "user_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for evaluasi
-- ----------------------------
DROP TABLE IF EXISTS "public"."evaluasi";
CREATE TABLE "public"."evaluasi" (
  "evaluasi_id" int4 NOT NULL DEFAULT nextval('evaluasi_evaluasi_id_seq'::regclass),
  "evaluasi_kps_id" int4,
  "evaluasi_tahun" varchar(10) COLLATE "pg_catalog"."default",
  "evaluasi_status" varchar(50) COLLATE "pg_catalog"."default",
  "evaluasi_hasil" varchar(50) COLLATE "pg_catalog"."default",
  "evaluasi_waktu_upload" timestamp(6),
  "evaluasi_petugas" int4,
  "evaluasi_tanggal" timestamp(6),
  "file_attachments" text COLLATE "pg_catalog"."default",
  "evaluasi_pendamping_id" int4
)
;

-- ----------------------------
-- Table structure for evaluasi_detail
-- ----------------------------
DROP TABLE IF EXISTS "public"."evaluasi_detail";
CREATE TABLE "public"."evaluasi_detail" (
  "detail_id" int4 NOT NULL DEFAULT nextval('evaluasi_detail_detail_id_seq'::regclass),
  "evaluasi_id" int4 NOT NULL,
  "kriteria_id" int4 NOT NULL,
  "jawaban" bool NOT NULL DEFAULT false,
  "nilai" numeric(5,2) NOT NULL DEFAULT 0,
  "deskripsi" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for kabupaten
-- ----------------------------
DROP TABLE IF EXISTS "public"."kabupaten";
CREATE TABLE "public"."kabupaten" (
  "kabupaten_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "provinsi_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "kabupaten_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for kategori
-- ----------------------------
DROP TABLE IF EXISTS "public"."kategori";
CREATE TABLE "public"."kategori" (
  "kategori_id" int4 NOT NULL DEFAULT nextval('kategori_kategori_id_seq'::regclass),
  "kategori_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "kategori_keterangan" text COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for kecamatan
-- ----------------------------
DROP TABLE IF EXISTS "public"."kecamatan";
CREATE TABLE "public"."kecamatan" (
  "kecamatan_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "kabupaten_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "kecamatan_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for kelurahan
-- ----------------------------
DROP TABLE IF EXISTS "public"."kelurahan";
CREATE TABLE "public"."kelurahan" (
  "kelurahan_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "kecamatan_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "kelurahan_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for kinerja_kps
-- ----------------------------
DROP TABLE IF EXISTS "public"."kinerja_kps";
CREATE TABLE "public"."kinerja_kps" (
  "kinerja_kps_id" int4 NOT NULL DEFAULT nextval('kinerja_kps_kinerja_kps_id_seq'::regclass),
  "kinerja_kps_kps_id" int4,
  "kinerja_kps_pendamping_id" int4,
  "kinerja_kps_waktu_upload" timestamp(6),
  "kinerja_kps_komoditas" varchar(50) COLLATE "pg_catalog"."default",
  "kinerja_kps_kelas_kups" varchar(50) COLLATE "pg_catalog"."default",
  "kinerja_kps_nilai_transaksi" numeric(18,2),
  "kinerja_kps_prestasi" varchar(50) COLLATE "pg_catalog"."default",
  "kinerja_kps_mitra_kerjasama" varchar(50) COLLATE "pg_catalog"."default",
  "kinerja_kps_petugas" int4
)
;

-- ----------------------------
-- Table structure for master_apresiasi_pemda_kriteria
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_apresiasi_pemda_kriteria";
CREATE TABLE "public"."master_apresiasi_pemda_kriteria" (
  "kriteria_id" int4 NOT NULL DEFAULT nextval('master_apresiasi_pemda_kriteria_kriteria_id_seq'::regclass),
  "kriteria_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "kriteria_deskripsi" text COLLATE "pg_catalog"."default",
  "bobot" numeric(5,2) NOT NULL,
  "urutan" int4 NOT NULL DEFAULT 0,
  "is_active" bool NOT NULL DEFAULT true,
  "versi" int4 NOT NULL DEFAULT 1,
  "versi_aktif" bool NOT NULL DEFAULT true,
  "kriteria_id_parent" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_bps
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_bps";
CREATE TABLE "public"."master_bps" (
  "nama_bps" varchar(255) COLLATE "pg_catalog"."default",
  "address" text COLLATE "pg_catalog"."default",
  "provinsi_id" varchar(10) COLLATE "pg_catalog"."default",
  "kab_kota_id" varchar(10) COLLATE "pg_catalog"."default",
  "kecamatan_id" varchar(10) COLLATE "pg_catalog"."default",
  "kelurahan_id" varchar(10) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "bps_id" int4 NOT NULL DEFAULT nextval('master_bps_bps_id_seq'::regclass),
  "kode_balai" varchar(50) COLLATE "pg_catalog"."default",
  "wilayah_kerja" jsonb
)
;

-- ----------------------------
-- Table structure for master_kategori_lampiran_pengawasan
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kategori_lampiran_pengawasan";
CREATE TABLE "public"."master_kategori_lampiran_pengawasan" (
  "kategori_id" int4 NOT NULL DEFAULT nextval('master_kategori_lampiran_pengawasan_kategori_id_seq'::regclass),
  "nama_kategori" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "deskripsi" text COLLATE "pg_catalog"."default",
  "urutan" int4 NOT NULL DEFAULT 0,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_kategori_sertifikat
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kategori_sertifikat";
CREATE TABLE "public"."master_kategori_sertifikat" (
  "kategori_id" int4 NOT NULL DEFAULT nextval('master_kategori_sertifikat_kategori_id_seq'::regclass),
  "nama_kategori" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "deskripsi" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_kps
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kps";
CREATE TABLE "public"."master_kps" (
  "schema" text COLLATE "pg_catalog"."default",
  "agroforestry" text COLLATE "pg_catalog"."default",
  "ekosistem" text COLLATE "pg_catalog"."default",
  "file_peta" text COLLATE "pg_catalog"."default",
  "file_sk" text COLLATE "pg_catalog"."default",
  "flora_endemik" text COLLATE "pg_catalog"."default",
  "hd_id" text COLLATE "pg_catalog"."default",
  "hhbk" text COLLATE "pg_catalog"."default",
  "hhk" text COLLATE "pg_catalog"."default",
  "hkm_id" text COLLATE "pg_catalog"."default",
  "htr_id" text COLLATE "pg_catalog"."default",
  "id_kab" text COLLATE "pg_catalog"."default",
  "id_prov" text COLLATE "pg_catalog"."default",
  "id_usulan" text COLLATE "pg_catalog"."default",
  "jasling" text COLLATE "pg_catalog"."default",
  "jenis_kps" text COLLATE "pg_catalog"."default",
  "jml_kk_kps" text COLLATE "pg_catalog"."default",
  "jml_kk_pria" text COLLATE "pg_catalog"."default",
  "jml_kk_wanita" text COLLATE "pg_catalog"."default",
  "luas_gambut" numeric(18,2),
  "luas_hl" numeric(18,2),
  "luas_hp" numeric(18,2),
  "luas_hpk" numeric(18,2),
  "luas_hpt" numeric(18,2),
  "luas_mangrove" numeric(18,2),
  "luas_sk" numeric(18,2),
  "nama_das" text COLLATE "pg_catalog"."default",
  "nama_desa" text COLLATE "pg_catalog"."default",
  "nama_kab" text COLLATE "pg_catalog"."default",
  "nama_kec" text COLLATE "pg_catalog"."default",
  "nama_kontak_kps" text COLLATE "pg_catalog"."default",
  "nama_kph" text COLLATE "pg_catalog"."default",
  "nama_kps" text COLLATE "pg_catalog"."default",
  "nama_prov" text COLLATE "pg_catalog"."default",
  "no_kontak_kps" text COLLATE "pg_catalog"."default",
  "no_sk_normalized" text COLLATE "pg_catalog"."default",
  "perikanan" text COLLATE "pg_catalog"."default",
  "peternakan" text COLLATE "pg_catalog"."default",
  "satwa_endemik" text COLLATE "pg_catalog"."default",
  "stok_karbon" numeric(18,2),
  "tgl_sk" timestamp(6),
  "bps_id" int4,
  "created_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "kps_das" varchar(512) COLLATE "pg_catalog"."default",
  "kps_desa" varchar(512) COLLATE "pg_catalog"."default",
  "kps_file_peta" varchar(512) COLLATE "pg_catalog"."default",
  "kps_file_sk" varchar(512) COLLATE "pg_catalog"."default",
  "kps_id" int4,
  "kps_jenis" varchar(512) COLLATE "pg_catalog"."default",
  "kps_jml_kk" varchar(50) COLLATE "pg_catalog"."default",
  "kps_kab" varchar(512) COLLATE "pg_catalog"."default",
  "kps_keterangan" varchar(512) COLLATE "pg_catalog"."default",
  "kps_kode" varchar(512) COLLATE "pg_catalog"."default",
  "kps_kontak_nama" varchar(512) COLLATE "pg_catalog"."default",
  "kps_kontak_no" varchar(100) COLLATE "pg_catalog"."default",
  "kps_kph" varchar(512) COLLATE "pg_catalog"."default",
  "kps_luas" varchar(100) COLLATE "pg_catalog"."default",
  "kps_metadata" jsonb,
  "kps_nama" varchar(512) COLLATE "pg_catalog"."default",
  "kps_petugas" varchar(512) COLLATE "pg_catalog"."default",
  "kps_provinsi" varchar(512) COLLATE "pg_catalog"."default",
  "kps_seksi" varchar(512) COLLATE "pg_catalog"."default",
  "kps_tahun" varchar(512) COLLATE "pg_catalog"."default",
  "kps_waktu_upload" varchar(512) COLLATE "pg_catalog"."default",
  "updated_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "id" int4 NOT NULL DEFAULT nextval('master_kps_id_seq'::regclass),
  "no_sk_pkps" text COLLATE "pg_catalog"."default",
  "is_folu" bool DEFAULT false,
  "id_pkps" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for master_kriteria
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kriteria";
CREATE TABLE "public"."master_kriteria" (
  "kriteria_id" int4 NOT NULL DEFAULT nextval('master_kriteria_kriteria_id_seq'::regclass),
  "tipe_kriteria" int4 NOT NULL,
  "kriteria_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "kriteria_deskripsi" text COLLATE "pg_catalog"."default",
  "bobot" numeric(5,2) NOT NULL,
  "urutan" int4 NOT NULL DEFAULT 0,
  "is_active" bool NOT NULL DEFAULT true,
  "versi" int4 NOT NULL DEFAULT 1,
  "versi_aktif" bool NOT NULL DEFAULT true,
  "kriteria_id_parent" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_kriteria_kategori
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kriteria_kategori";
CREATE TABLE "public"."master_kriteria_kategori" (
  "kategori_id" int4 NOT NULL DEFAULT nextval('master_kriteria_kategori_kategori_id_seq'::regclass),
  "tipe_kriteria" int4 NOT NULL,
  "kategori_nama" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "min_score" numeric(10,2) NOT NULL,
  "max_score" numeric(10,2) NOT NULL,
  "urutan" int4 NOT NULL DEFAULT 0,
  "warna" varchar(50) COLLATE "pg_catalog"."default",
  "is_active" bool NOT NULL DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_kriteria_tipe
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kriteria_tipe";
CREATE TABLE "public"."master_kriteria_tipe" (
  "tipe_id" int4 NOT NULL DEFAULT nextval('master_kriteria_tipe_tipe_id_seq'::regclass),
  "tipe_nama" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "tipe_kode" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "is_active" bool NOT NULL DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_kups
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_kups";
CREATE TABLE "public"."master_kups" (
  "kups_id" int4 NOT NULL DEFAULT nextval('master_kups_kups_id_seq'::regclass),
  "external_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "lintang" numeric(18,8),
  "nujur" numeric(18,8),
  "nama_kups" varchar(255) COLLATE "pg_catalog"."default",
  "kelas_kups" varchar(50) COLLATE "pg_catalog"."default",
  "potensi" jsonb,
  "produk" jsonb,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for master_pemda
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_pemda";
CREATE TABLE "public"."master_pemda" (
  "pemda_id" int4 NOT NULL DEFAULT nextval('master_pemda_pemda_id_seq'::regclass),
  "nama_pemda" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "alamat_kantor" text COLLATE "pg_catalog"."default",
  "provinsi_id" varchar(10) COLLATE "pg_catalog"."default",
  "kab_kota_id" varchar(10) COLLATE "pg_catalog"."default",
  "kecamatan_id" varchar(10) COLLATE "pg_catalog"."default",
  "kelurahan_id" varchar(10) COLLATE "pg_catalog"."default",
  "nama_kontak" varchar(255) COLLATE "pg_catalog"."default",
  "no_tlp" varchar(50) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "bps_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "kategori" varchar(50) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for master_pendamping
-- ----------------------------
DROP TABLE IF EXISTS "public"."master_pendamping";
CREATE TABLE "public"."master_pendamping" (
  "pendamping_id" int4 NOT NULL DEFAULT nextval('master_pendamping_pendamping_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "kategori" varchar(255) COLLATE "pg_catalog"."default",
  "pendidikan" varchar(255) COLLATE "pg_catalog"."default",
  "provinsi" varchar(255) COLLATE "pg_catalog"."default",
  "kabupaten_kota" varchar(255) COLLATE "pg_catalog"."default",
  "kecamatan" varchar(255) COLLATE "pg_catalog"."default",
  "desa_kelurahan" varchar(255) COLLATE "pg_catalog"."default",
  "sumber_pembiayaan" varchar(255) COLLATE "pg_catalog"."default",
  "pekerjaan_pendamping" varchar(255) COLLATE "pg_catalog"."default",
  "status_pendamping" varchar(50) COLLATE "pg_catalog"."default",
  "jenis_kelamin" varchar(50) COLLATE "pg_catalog"."default",
  "nik" varchar(50) COLLATE "pg_catalog"."default",
  "no_hp" varchar(50) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "kab_kota_id" varchar(10) COLLATE "pg_catalog"."default",
  "kecamatan_id" varchar(10) COLLATE "pg_catalog"."default",
  "kelurahan_id" varchar(10) COLLATE "pg_catalog"."default",
  "provinsi_id" varchar(10) COLLATE "pg_catalog"."default",
  "status_lms" varchar(50) COLLATE "pg_catalog"."default",
  "no_sk" varchar(255) COLLATE "pg_catalog"."default",
  "is_local_champion" bool DEFAULT false
)
;

-- ----------------------------
-- Table structure for pemantauan
-- ----------------------------
DROP TABLE IF EXISTS "public"."pemantauan";
CREATE TABLE "public"."pemantauan" (
  "pemantauan_id" int4 NOT NULL DEFAULT nextval('pemantauan_pemantauan_id_seq'::regclass),
  "pemantauan_kps_id" int4,
  "pemantauan_tahun" varchar(10) COLLATE "pg_catalog"."default",
  "pemantauan_status" varchar(50) COLLATE "pg_catalog"."default",
  "pemantauan_hasil" varchar(50) COLLATE "pg_catalog"."default",
  "pemantauan_waktu_upload" timestamp(6),
  "pemantauan_petugas" int4,
  "file_attachments" text COLLATE "pg_catalog"."default",
  "pemantauan_luas_areal" numeric(18,2),
  "pemantauan_umur_areal" varchar(50) COLLATE "pg_catalog"."default",
  "pemantauan_jenis_areal" varchar(50) COLLATE "pg_catalog"."default",
  "pemantauan_sudah_jangka_benah" varchar(50) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for pendampingan
-- ----------------------------
DROP TABLE IF EXISTS "public"."pendampingan";
CREATE TABLE "public"."pendampingan" (
  "id_pendampingan" int4 NOT NULL DEFAULT nextval('pendampingan_pendampingan_id_seq'::regclass),
  "pendamping_id" int4,
  "waktu_upload" timestamp(6),
  "tahun_pendampingan" varchar(1000) COLLATE "pg_catalog"."default",
  "kps_id" int4,
  "keterangan" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" int4,
  "file_attachments" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for pengawasan
-- ----------------------------
DROP TABLE IF EXISTS "public"."pengawasan";
CREATE TABLE "public"."pengawasan" (
  "pengawasan_id" int4 NOT NULL DEFAULT nextval('pengawasan_pengawasan_id_seq'::regclass),
  "pengawasan_kps_id" int4,
  "pengawasan_tahun" varchar(10) COLLATE "pg_catalog"."default",
  "pengawasan_status" varchar(50) COLLATE "pg_catalog"."default",
  "pengawasan_sanksi_adm" varchar(50) COLLATE "pg_catalog"."default",
  "pengawasan_waktu_upload" timestamp(6),
  "pengawasan_petugas" int4,
  "pengawasan_sanksi_jlh" int4,
  "pengawasan_jlh" varchar(50) COLLATE "pg_catalog"."default",
  "file_attachments" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."permissions";
CREATE TABLE "public"."permissions" (
  "permission_id" int4 NOT NULL DEFAULT nextval('permissions_permission_id_seq'::regclass),
  "permission_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "permission_description" varchar(255) COLLATE "pg_catalog"."default",
  "resource" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "action" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for pesan_kps
-- ----------------------------
DROP TABLE IF EXISTS "public"."pesan_kps";
CREATE TABLE "public"."pesan_kps" (
  "pesan_kps_id" int4 NOT NULL DEFAULT nextval('pesan_kps_pesan_kps_id_seq'::regclass),
  "klasifikasi" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "judul" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "isi" text COLLATE "pg_catalog"."default" NOT NULL,
  "tanggal_kejadian" date,
  "lokasi_kejadian" varchar(255) COLLATE "pg_catalog"."default",
  "instansi_tujuan" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "kps_id" int4
)
;

-- ----------------------------
-- Table structure for provinsi
-- ----------------------------
DROP TABLE IF EXISTS "public"."provinsi";
CREATE TABLE "public"."provinsi" (
  "provinsi_id" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "provinsi_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for publikasi
-- ----------------------------
DROP TABLE IF EXISTS "public"."publikasi";
CREATE TABLE "public"."publikasi" (
  "publikasi_id" int4 NOT NULL DEFAULT nextval('publikasi_publikasi_id_seq'::regclass),
  "judul_utama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "judul_lengkap" text COLLATE "pg_catalog"."default" NOT NULL,
  "detail_tambahan" text COLLATE "pg_catalog"."default",
  "kategori" varchar(100) COLLATE "pg_catalog"."default",
  "tahun" varchar(50) COLLATE "pg_catalog"."default",
  "thumbnail_url" text COLLATE "pg_catalog"."default",
  "file_url" text COLLATE "pg_catalog"."default",
  "is_active" bool NOT NULL DEFAULT true,
  "user_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for riwayat
-- ----------------------------
DROP TABLE IF EXISTS "public"."riwayat";
CREATE TABLE "public"."riwayat" (
  "riwayat_id" int4 NOT NULL DEFAULT nextval('riwayat_riwayat_id_seq'::regclass),
  "riwayat_waktu" timestamp(6) NOT NULL,
  "riwayat_user" int4 NOT NULL,
  "riwayat_arsip" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for role_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."role_permissions";
CREATE TABLE "public"."role_permissions" (
  "role_permission_id" int4 NOT NULL DEFAULT nextval('role_permissions_role_permission_id_seq'::regclass),
  "role_id" int4 NOT NULL,
  "permission_id" int4 NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."roles";
CREATE TABLE "public"."roles" (
  "role_id" int4 NOT NULL DEFAULT nextval('roles_role_id_seq'::regclass),
  "role_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "role_description" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for sertifikat_pendamping
-- ----------------------------
DROP TABLE IF EXISTS "public"."sertifikat_pendamping";
CREATE TABLE "public"."sertifikat_pendamping" (
  "sertifikat_id" int4 NOT NULL DEFAULT nextval('sertifikat_pendamping_sertifikat_id_seq'::regclass),
  "pendamping_id" int4 NOT NULL,
  "kategori_sertifikat" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "nomor_sertifikat" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "tanggal_expired" date,
  "file_sertifikat" text COLLATE "pg_catalog"."default",
  "deskripsi" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for settings
-- ----------------------------
DROP TABLE IF EXISTS "public"."settings";
CREATE TABLE "public"."settings" (
  "setting_id" int4 NOT NULL DEFAULT nextval('settings_setting_id_seq'::regclass),
  "setting_key" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "setting_value" text COLLATE "pg_catalog"."default" NOT NULL,
  "setting_type" "public"."SettingType" NOT NULL DEFAULT 'string'::"SettingType",
  "category" "public"."SettingCategory" NOT NULL DEFAULT 'general'::"SettingCategory",
  "label" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for user_roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_roles";
CREATE TABLE "public"."user_roles" (
  "user_role_id" int4 NOT NULL DEFAULT nextval('user_roles_user_role_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "role_id" int4 NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "user_id" int4 NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
  "user_nama" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_foto" text COLLATE "pg_catalog"."default",
  "user_type" "public"."UserType" NOT NULL DEFAULT 'user'::"UserType",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL,
  "user_email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'aktif'::character varying,
  "verification_token" varchar(255) COLLATE "pg_catalog"."default",
  "verification_token_expires" timestamp(6),
  "bps_id" int4
)
;

-- ----------------------------
-- Function structure for update_updated_at_column
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."update_updated_at_column"();
CREATE FUNCTION "public"."update_updated_at_column"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
      BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
      END;
      $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."apresiasi_apresiasi_id_seq"
OWNED BY "public"."apresiasi"."apresiasi_id";
SELECT setval('"public"."apresiasi_apresiasi_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."apresiasi_pemda_apresiasi_pemda_id_seq"
OWNED BY "public"."apresiasi_pemda"."apresiasi_pemda_id";
SELECT setval('"public"."apresiasi_pemda_apresiasi_pemda_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."apresiasi_pemda_detail_detail_id_seq"
OWNED BY "public"."apresiasi_pemda_detail"."detail_id";
SELECT setval('"public"."apresiasi_pemda_detail_detail_id_seq"', 16, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."arsip_arsip_id_seq"
OWNED BY "public"."arsip"."arsip_id";
SELECT setval('"public"."arsip_arsip_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."banners_banner_id_seq"
OWNED BY "public"."banners"."banner_id";
SELECT setval('"public"."banners_banner_id_seq"', 11, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."berita_berita_id_seq"
OWNED BY "public"."berita"."berita_id";
SELECT setval('"public"."berita_berita_id_seq"', 25, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."buku_buku_id_seq"
OWNED BY "public"."buku"."buku_id";
SELECT setval('"public"."buku_buku_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."evaluasi_detail_detail_id_seq"
OWNED BY "public"."evaluasi_detail"."detail_id";
SELECT setval('"public"."evaluasi_detail_detail_id_seq"', 4, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."evaluasi_evaluasi_id_seq"
OWNED BY "public"."evaluasi"."evaluasi_id";
SELECT setval('"public"."evaluasi_evaluasi_id_seq"', 10951, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."kategori_kategori_id_seq"
OWNED BY "public"."kategori"."kategori_id";
SELECT setval('"public"."kategori_kategori_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."kinerja_kps_kinerja_kps_id_seq"
OWNED BY "public"."kinerja_kps"."kinerja_kps_id";
SELECT setval('"public"."kinerja_kps_kinerja_kps_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_apresiasi_pemda_kriteria_kriteria_id_seq"
OWNED BY "public"."master_apresiasi_pemda_kriteria"."kriteria_id";
SELECT setval('"public"."master_apresiasi_pemda_kriteria_kriteria_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_bps_bps_id_seq"
OWNED BY "public"."master_bps"."bps_id";
SELECT setval('"public"."master_bps_bps_id_seq"', 26, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kategori_lampiran_pengawasan_kategori_id_seq"
OWNED BY "public"."master_kategori_lampiran_pengawasan"."kategori_id";
SELECT setval('"public"."master_kategori_lampiran_pengawasan_kategori_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kategori_sertifikat_kategori_id_seq"
OWNED BY "public"."master_kategori_sertifikat"."kategori_id";
SELECT setval('"public"."master_kategori_sertifikat_kategori_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kps_id_seq"
OWNED BY "public"."master_kps"."id";
SELECT setval('"public"."master_kps_id_seq"', 17786, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kriteria_kategori_kategori_id_seq"
OWNED BY "public"."master_kriteria_kategori"."kategori_id";
SELECT setval('"public"."master_kriteria_kategori_kategori_id_seq"', 6, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kriteria_kriteria_id_seq"
OWNED BY "public"."master_kriteria"."kriteria_id";
SELECT setval('"public"."master_kriteria_kriteria_id_seq"', 16, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kriteria_tipe_tipe_id_seq"
OWNED BY "public"."master_kriteria_tipe"."tipe_id";
SELECT setval('"public"."master_kriteria_tipe_tipe_id_seq"', 9, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_kups_kups_id_seq"
OWNED BY "public"."master_kups"."kups_id";
SELECT setval('"public"."master_kups_kups_id_seq"', 11103, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_pemda_pemda_id_seq"
OWNED BY "public"."master_pemda"."pemda_id";
SELECT setval('"public"."master_pemda_pemda_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."master_pendamping_pendamping_id_seq"
OWNED BY "public"."master_pendamping"."pendamping_id";
SELECT setval('"public"."master_pendamping_pendamping_id_seq"', 3926, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."pemantauan_pemantauan_id_seq"
OWNED BY "public"."pemantauan"."pemantauan_id";
SELECT setval('"public"."pemantauan_pemantauan_id_seq"', 201, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."pendampingan_pendampingan_id_seq"
OWNED BY "public"."pendampingan"."id_pendampingan";
SELECT setval('"public"."pendampingan_pendampingan_id_seq"', 9164, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."pengawasan_pengawasan_id_seq"
OWNED BY "public"."pengawasan"."pengawasan_id";
SELECT setval('"public"."pengawasan_pengawasan_id_seq"', 198, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."permissions_permission_id_seq"
OWNED BY "public"."permissions"."permission_id";
SELECT setval('"public"."permissions_permission_id_seq"', 161, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."pesan_kps_pesan_kps_id_seq"
OWNED BY "public"."pesan_kps"."pesan_kps_id";
SELECT setval('"public"."pesan_kps_pesan_kps_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."publikasi_publikasi_id_seq"
OWNED BY "public"."publikasi"."publikasi_id";
SELECT setval('"public"."publikasi_publikasi_id_seq"', 4, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."riwayat_riwayat_id_seq"
OWNED BY "public"."riwayat"."riwayat_id";
SELECT setval('"public"."riwayat_riwayat_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."role_permissions_role_permission_id_seq"
OWNED BY "public"."role_permissions"."role_permission_id";
SELECT setval('"public"."role_permissions_role_permission_id_seq"', 700, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."roles_role_id_seq"
OWNED BY "public"."roles"."role_id";
SELECT setval('"public"."roles_role_id_seq"', 6, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."sertifikat_pendamping_sertifikat_id_seq"
OWNED BY "public"."sertifikat_pendamping"."sertifikat_id";
SELECT setval('"public"."sertifikat_pendamping_sertifikat_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."settings_setting_id_seq"
OWNED BY "public"."settings"."setting_id";
SELECT setval('"public"."settings_setting_id_seq"', 37, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."user_roles_user_role_id_seq"
OWNED BY "public"."user_roles"."user_role_id";
SELECT setval('"public"."user_roles_user_role_id_seq"', 4007, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_user_id_seq"
OWNED BY "public"."users"."user_id";
SELECT setval('"public"."users_user_id_seq"', 3991, true);

-- ----------------------------
-- Primary Key structure for table _prisma_migrations
-- ----------------------------
ALTER TABLE "public"."_prisma_migrations" ADD CONSTRAINT "_prisma_migrations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table apresiasi
-- ----------------------------
ALTER TABLE "public"."apresiasi" ADD CONSTRAINT "apresiasi_pkey" PRIMARY KEY ("apresiasi_id");

-- ----------------------------
-- Indexes structure for table apresiasi_pemda
-- ----------------------------
CREATE INDEX "apresiasi_pemda_pemda_id_tahun_versi_kriteria_idx" ON "public"."apresiasi_pemda" USING btree (
  "pemda_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "tahun" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "versi_kriteria" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "apresiasi_pemda_tahun_idx" ON "public"."apresiasi_pemda" USING btree (
  "tahun" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table apresiasi_pemda
-- ----------------------------
ALTER TABLE "public"."apresiasi_pemda" ADD CONSTRAINT "apresiasi_pemda_pkey" PRIMARY KEY ("apresiasi_pemda_id");

-- ----------------------------
-- Indexes structure for table apresiasi_pemda_detail
-- ----------------------------
CREATE INDEX "apresiasi_pemda_detail_apresiasi_pemda_id_kriteria_id_krite_idx" ON "public"."apresiasi_pemda_detail" USING btree (
  "apresiasi_pemda_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "kriteria_versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "apresiasi_pemda_detail_apresiasi_pemda_id_kriteria_id_krite_key" ON "public"."apresiasi_pemda_detail" USING btree (
  "apresiasi_pemda_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "kriteria_versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table apresiasi_pemda_detail
-- ----------------------------
ALTER TABLE "public"."apresiasi_pemda_detail" ADD CONSTRAINT "apresiasi_pemda_detail_pkey" PRIMARY KEY ("detail_id");

-- ----------------------------
-- Primary Key structure for table arsip
-- ----------------------------
ALTER TABLE "public"."arsip" ADD CONSTRAINT "arsip_pkey" PRIMARY KEY ("arsip_id");

-- ----------------------------
-- Triggers structure for table banners
-- ----------------------------
CREATE TRIGGER "update_banners_updated_at" BEFORE UPDATE ON "public"."banners"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_updated_at_column"();

-- ----------------------------
-- Primary Key structure for table banners
-- ----------------------------
ALTER TABLE "public"."banners" ADD CONSTRAINT "banners_pkey" PRIMARY KEY ("banner_id");

-- ----------------------------
-- Indexes structure for table berita
-- ----------------------------
CREATE UNIQUE INDEX "berita_slug_key" ON "public"."berita" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
) WHERE slug IS NOT NULL;

-- ----------------------------
-- Triggers structure for table berita
-- ----------------------------
CREATE TRIGGER "update_berita_updated_at" BEFORE UPDATE ON "public"."berita"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_updated_at_column"();

-- ----------------------------
-- Primary Key structure for table berita
-- ----------------------------
ALTER TABLE "public"."berita" ADD CONSTRAINT "berita_pkey" PRIMARY KEY ("berita_id");

-- ----------------------------
-- Primary Key structure for table buku
-- ----------------------------
ALTER TABLE "public"."buku" ADD CONSTRAINT "buku_pkey" PRIMARY KEY ("buku_id");

-- ----------------------------
-- Primary Key structure for table evaluasi
-- ----------------------------
ALTER TABLE "public"."evaluasi" ADD CONSTRAINT "evaluasi_pkey" PRIMARY KEY ("evaluasi_id");

-- ----------------------------
-- Indexes structure for table evaluasi_detail
-- ----------------------------
CREATE INDEX "evaluasi_detail_evaluasi_id_idx" ON "public"."evaluasi_detail" USING btree (
  "evaluasi_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "evaluasi_detail_kriteria_id_idx" ON "public"."evaluasi_detail" USING btree (
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table evaluasi_detail
-- ----------------------------
ALTER TABLE "public"."evaluasi_detail" ADD CONSTRAINT "evaluasi_detail_pkey" PRIMARY KEY ("detail_id");

-- ----------------------------
-- Indexes structure for table kabupaten
-- ----------------------------
CREATE INDEX "kabupaten_provinsi_id_idx" ON "public"."kabupaten" USING btree (
  "provinsi_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table kabupaten
-- ----------------------------
ALTER TABLE "public"."kabupaten" ADD CONSTRAINT "kabupaten_pkey" PRIMARY KEY ("kabupaten_id");

-- ----------------------------
-- Primary Key structure for table kategori
-- ----------------------------
ALTER TABLE "public"."kategori" ADD CONSTRAINT "kategori_pkey" PRIMARY KEY ("kategori_id");

-- ----------------------------
-- Indexes structure for table kecamatan
-- ----------------------------
CREATE INDEX "kecamatan_kabupaten_id_idx" ON "public"."kecamatan" USING btree (
  "kabupaten_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table kecamatan
-- ----------------------------
ALTER TABLE "public"."kecamatan" ADD CONSTRAINT "kecamatan_pkey" PRIMARY KEY ("kecamatan_id");

-- ----------------------------
-- Indexes structure for table kelurahan
-- ----------------------------
CREATE INDEX "kelurahan_kecamatan_id_idx" ON "public"."kelurahan" USING btree (
  "kecamatan_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table kelurahan
-- ----------------------------
ALTER TABLE "public"."kelurahan" ADD CONSTRAINT "kelurahan_pkey" PRIMARY KEY ("kelurahan_id");

-- ----------------------------
-- Primary Key structure for table kinerja_kps
-- ----------------------------
ALTER TABLE "public"."kinerja_kps" ADD CONSTRAINT "kinerja_kps_pkey" PRIMARY KEY ("kinerja_kps_id");

-- ----------------------------
-- Indexes structure for table master_apresiasi_pemda_kriteria
-- ----------------------------
CREATE INDEX "master_apresiasi_pemda_kriteria_kriteria_id_versi_idx" ON "public"."master_apresiasi_pemda_kriteria" USING btree (
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "master_apresiasi_pemda_kriteria_kriteria_id_versi_key" ON "public"."master_apresiasi_pemda_kriteria" USING btree (
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "master_apresiasi_pemda_kriteria_versi_aktif_idx" ON "public"."master_apresiasi_pemda_kriteria" USING btree (
  "versi_aktif" "pg_catalog"."bool_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_apresiasi_pemda_kriteria
-- ----------------------------
ALTER TABLE "public"."master_apresiasi_pemda_kriteria" ADD CONSTRAINT "master_apresiasi_pemda_kriteria_pkey" PRIMARY KEY ("kriteria_id");

-- ----------------------------
-- Primary Key structure for table master_bps
-- ----------------------------
ALTER TABLE "public"."master_bps" ADD CONSTRAINT "master_bps_pkey" PRIMARY KEY ("bps_id");

-- ----------------------------
-- Primary Key structure for table master_kategori_lampiran_pengawasan
-- ----------------------------
ALTER TABLE "public"."master_kategori_lampiran_pengawasan" ADD CONSTRAINT "master_kategori_lampiran_pengawasan_pkey" PRIMARY KEY ("kategori_id");

-- ----------------------------
-- Indexes structure for table master_kategori_sertifikat
-- ----------------------------
CREATE UNIQUE INDEX "master_kategori_sertifikat_nama_kategori_key" ON "public"."master_kategori_sertifikat" USING btree (
  "nama_kategori" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kategori_sertifikat
-- ----------------------------
ALTER TABLE "public"."master_kategori_sertifikat" ADD CONSTRAINT "master_kategori_sertifikat_pkey" PRIMARY KEY ("kategori_id");

-- ----------------------------
-- Indexes structure for table master_kps
-- ----------------------------
CREATE UNIQUE INDEX "master_kps_kps_id_key" ON "public"."master_kps" USING btree (
  "kps_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kps
-- ----------------------------
ALTER TABLE "public"."master_kps" ADD CONSTRAINT "master_kps_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table master_kriteria
-- ----------------------------
CREATE INDEX "master_kriteria_kriteria_id_versi_idx" ON "public"."master_kriteria" USING btree (
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "master_kriteria_kriteria_id_versi_key" ON "public"."master_kriteria" USING btree (
  "kriteria_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "versi" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "master_kriteria_tipe_kriteria_idx" ON "public"."master_kriteria" USING btree (
  "tipe_kriteria" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "master_kriteria_tipe_kriteria_versi_aktif_idx" ON "public"."master_kriteria" USING btree (
  "tipe_kriteria" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "versi_aktif" "pg_catalog"."bool_ops" ASC NULLS LAST
);
CREATE INDEX "master_kriteria_versi_aktif_idx" ON "public"."master_kriteria" USING btree (
  "versi_aktif" "pg_catalog"."bool_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kriteria
-- ----------------------------
ALTER TABLE "public"."master_kriteria" ADD CONSTRAINT "master_kriteria_pkey" PRIMARY KEY ("kriteria_id");

-- ----------------------------
-- Indexes structure for table master_kriteria_kategori
-- ----------------------------
CREATE INDEX "master_kriteria_kategori_tipe_kriteria_idx" ON "public"."master_kriteria_kategori" USING btree (
  "tipe_kriteria" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "master_kriteria_kategori_tipe_kriteria_min_score_max_score_idx" ON "public"."master_kriteria_kategori" USING btree (
  "tipe_kriteria" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "min_score" "pg_catalog"."numeric_ops" ASC NULLS LAST,
  "max_score" "pg_catalog"."numeric_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kriteria_kategori
-- ----------------------------
ALTER TABLE "public"."master_kriteria_kategori" ADD CONSTRAINT "master_kriteria_kategori_pkey" PRIMARY KEY ("kategori_id");

-- ----------------------------
-- Indexes structure for table master_kriteria_tipe
-- ----------------------------
CREATE UNIQUE INDEX "master_kriteria_tipe_tipe_kode_key" ON "public"."master_kriteria_tipe" USING btree (
  "tipe_kode" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "master_kriteria_tipe_tipe_nama_key" ON "public"."master_kriteria_tipe" USING btree (
  "tipe_nama" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kriteria_tipe
-- ----------------------------
ALTER TABLE "public"."master_kriteria_tipe" ADD CONSTRAINT "master_kriteria_tipe_pkey" PRIMARY KEY ("tipe_id");

-- ----------------------------
-- Indexes structure for table master_kups
-- ----------------------------
CREATE INDEX "master_kups_external_id_idx" ON "public"."master_kups" USING btree (
  "external_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "master_kups_external_id_key" ON "public"."master_kups" USING btree (
  "external_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "master_kups_kelas_kups_idx" ON "public"."master_kups" USING btree (
  "kelas_kups" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "master_kups_nama_kups_idx" ON "public"."master_kups" USING btree (
  "nama_kups" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table master_kups
-- ----------------------------
ALTER TABLE "public"."master_kups" ADD CONSTRAINT "master_kups_pkey" PRIMARY KEY ("kups_id");

-- ----------------------------
-- Primary Key structure for table master_pemda
-- ----------------------------
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_pkey" PRIMARY KEY ("pemda_id");

-- ----------------------------
-- Uniques structure for table master_pendamping
-- ----------------------------
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_user_id_key" UNIQUE ("user_id");

-- ----------------------------
-- Primary Key structure for table master_pendamping
-- ----------------------------
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_pkey" PRIMARY KEY ("pendamping_id");

-- ----------------------------
-- Primary Key structure for table pemantauan
-- ----------------------------
ALTER TABLE "public"."pemantauan" ADD CONSTRAINT "pemantauan_pkey" PRIMARY KEY ("pemantauan_id");

-- ----------------------------
-- Primary Key structure for table pendampingan
-- ----------------------------
ALTER TABLE "public"."pendampingan" ADD CONSTRAINT "pendampingan_pkey" PRIMARY KEY ("id_pendampingan");

-- ----------------------------
-- Primary Key structure for table pengawasan
-- ----------------------------
ALTER TABLE "public"."pengawasan" ADD CONSTRAINT "pengawasan_pkey" PRIMARY KEY ("pengawasan_id");

-- ----------------------------
-- Indexes structure for table permissions
-- ----------------------------
CREATE UNIQUE INDEX "permissions_permission_name_key" ON "public"."permissions" USING btree (
  "permission_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "permissions_resource_action_key" ON "public"."permissions" USING btree (
  "resource" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "action" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table permissions
-- ----------------------------
ALTER TABLE "public"."permissions" ADD CONSTRAINT "permissions_pkey" PRIMARY KEY ("permission_id");

-- ----------------------------
-- Indexes structure for table pesan_kps
-- ----------------------------
CREATE INDEX "pesan_kps_created_at_idx" ON "public"."pesan_kps" USING btree (
  "created_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "pesan_kps_klasifikasi_idx" ON "public"."pesan_kps" USING btree (
  "klasifikasi" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "pesan_kps_kps_id_idx" ON "public"."pesan_kps" USING btree (
  "kps_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "pesan_kps_user_id_idx" ON "public"."pesan_kps" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table pesan_kps
-- ----------------------------
ALTER TABLE "public"."pesan_kps" ADD CONSTRAINT "pesan_kps_pkey" PRIMARY KEY ("pesan_kps_id");

-- ----------------------------
-- Primary Key structure for table provinsi
-- ----------------------------
ALTER TABLE "public"."provinsi" ADD CONSTRAINT "provinsi_pkey" PRIMARY KEY ("provinsi_id");

-- ----------------------------
-- Primary Key structure for table publikasi
-- ----------------------------
ALTER TABLE "public"."publikasi" ADD CONSTRAINT "publikasi_pkey" PRIMARY KEY ("publikasi_id");

-- ----------------------------
-- Primary Key structure for table riwayat
-- ----------------------------
ALTER TABLE "public"."riwayat" ADD CONSTRAINT "riwayat_pkey" PRIMARY KEY ("riwayat_id");

-- ----------------------------
-- Indexes structure for table role_permissions
-- ----------------------------
CREATE UNIQUE INDEX "role_permissions_role_id_permission_id_key" ON "public"."role_permissions" USING btree (
  "role_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "permission_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table role_permissions
-- ----------------------------
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_pkey" PRIMARY KEY ("role_permission_id");

-- ----------------------------
-- Indexes structure for table roles
-- ----------------------------
CREATE UNIQUE INDEX "roles_role_name_key" ON "public"."roles" USING btree (
  "role_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_pkey" PRIMARY KEY ("role_id");

-- ----------------------------
-- Indexes structure for table sertifikat_pendamping
-- ----------------------------
CREATE INDEX "sertifikat_pendamping_pendamping_id_idx" ON "public"."sertifikat_pendamping" USING btree (
  "pendamping_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table sertifikat_pendamping
-- ----------------------------
ALTER TABLE "public"."sertifikat_pendamping" ADD CONSTRAINT "sertifikat_pendamping_pkey" PRIMARY KEY ("sertifikat_id");

-- ----------------------------
-- Indexes structure for table settings
-- ----------------------------
CREATE INDEX "settings_category_idx" ON "public"."settings" USING btree (
  "category" "pg_catalog"."enum_ops" ASC NULLS LAST
);
CREATE INDEX "settings_setting_key_idx" ON "public"."settings" USING btree (
  "setting_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "settings_setting_key_key" ON "public"."settings" USING btree (
  "setting_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table settings
-- ----------------------------
ALTER TABLE "public"."settings" ADD CONSTRAINT "settings_pkey" PRIMARY KEY ("setting_id");

-- ----------------------------
-- Indexes structure for table user_roles
-- ----------------------------
CREATE UNIQUE INDEX "user_roles_user_id_role_id_key" ON "public"."user_roles" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "role_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table user_roles
-- ----------------------------
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_pkey" PRIMARY KEY ("user_role_id");

-- ----------------------------
-- Indexes structure for table users
-- ----------------------------
CREATE UNIQUE INDEX "users_user_email_key" ON "public"."users" USING btree (
  "user_email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Foreign Keys structure for table apresiasi
-- ----------------------------
ALTER TABLE "public"."apresiasi" ADD CONSTRAINT "apresiasi_apresiasi_petugas_fkey" FOREIGN KEY ("apresiasi_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table apresiasi_pemda
-- ----------------------------
ALTER TABLE "public"."apresiasi_pemda" ADD CONSTRAINT "apresiasi_pemda_apresiasi_petugas_fkey" FOREIGN KEY ("apresiasi_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."apresiasi_pemda" ADD CONSTRAINT "apresiasi_pemda_pemda_id_fkey" FOREIGN KEY ("pemda_id") REFERENCES "public"."master_pemda" ("pemda_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table apresiasi_pemda_detail
-- ----------------------------
ALTER TABLE "public"."apresiasi_pemda_detail" ADD CONSTRAINT "apresiasi_pemda_detail_apresiasi_pemda_id_fkey" FOREIGN KEY ("apresiasi_pemda_id") REFERENCES "public"."apresiasi_pemda" ("apresiasi_pemda_id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."apresiasi_pemda_detail" ADD CONSTRAINT "apresiasi_pemda_detail_kriteria_id_fkey" FOREIGN KEY ("kriteria_id") REFERENCES "public"."master_kriteria" ("kriteria_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table arsip
-- ----------------------------
ALTER TABLE "public"."arsip" ADD CONSTRAINT "arsip_arsip_kategori_fkey" FOREIGN KEY ("arsip_kategori") REFERENCES "public"."kategori" ("kategori_id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "public"."arsip" ADD CONSTRAINT "arsip_arsip_petugas_fkey" FOREIGN KEY ("arsip_petugas") REFERENCES "public"."users" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table berita
-- ----------------------------
ALTER TABLE "public"."berita" ADD CONSTRAINT "berita_published_admin_id_fkey" FOREIGN KEY ("published_admin_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."berita" ADD CONSTRAINT "berita_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table buku
-- ----------------------------
ALTER TABLE "public"."buku" ADD CONSTRAINT "buku_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table evaluasi
-- ----------------------------
ALTER TABLE "public"."evaluasi" ADD CONSTRAINT "evaluasi_evaluasi_pendamping_id_fkey" FOREIGN KEY ("evaluasi_pendamping_id") REFERENCES "public"."master_pendamping" ("pendamping_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."evaluasi" ADD CONSTRAINT "evaluasi_evaluasi_petugas_fkey" FOREIGN KEY ("evaluasi_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table evaluasi_detail
-- ----------------------------
ALTER TABLE "public"."evaluasi_detail" ADD CONSTRAINT "evaluasi_detail_evaluasi_id_fkey" FOREIGN KEY ("evaluasi_id") REFERENCES "public"."evaluasi" ("evaluasi_id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."evaluasi_detail" ADD CONSTRAINT "evaluasi_detail_kriteria_id_fkey" FOREIGN KEY ("kriteria_id") REFERENCES "public"."master_kriteria" ("kriteria_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table kabupaten
-- ----------------------------
ALTER TABLE "public"."kabupaten" ADD CONSTRAINT "kabupaten_provinsi_id_fkey" FOREIGN KEY ("provinsi_id") REFERENCES "public"."provinsi" ("provinsi_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table kecamatan
-- ----------------------------
ALTER TABLE "public"."kecamatan" ADD CONSTRAINT "kecamatan_kabupaten_id_fkey" FOREIGN KEY ("kabupaten_id") REFERENCES "public"."kabupaten" ("kabupaten_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table kelurahan
-- ----------------------------
ALTER TABLE "public"."kelurahan" ADD CONSTRAINT "kelurahan_kecamatan_id_fkey" FOREIGN KEY ("kecamatan_id") REFERENCES "public"."kecamatan" ("kecamatan_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table kinerja_kps
-- ----------------------------
ALTER TABLE "public"."kinerja_kps" ADD CONSTRAINT "kinerja_kps_kinerja_kps_petugas_fkey" FOREIGN KEY ("kinerja_kps_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_apresiasi_pemda_kriteria
-- ----------------------------
ALTER TABLE "public"."master_apresiasi_pemda_kriteria" ADD CONSTRAINT "master_apresiasi_pemda_kriteria_kriteria_id_parent_fkey" FOREIGN KEY ("kriteria_id_parent") REFERENCES "public"."master_apresiasi_pemda_kriteria" ("kriteria_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_bps
-- ----------------------------
ALTER TABLE "public"."master_bps" ADD CONSTRAINT "master_bps_kab_kota_id_fkey" FOREIGN KEY ("kab_kota_id") REFERENCES "public"."kabupaten" ("kabupaten_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_bps" ADD CONSTRAINT "master_bps_kecamatan_id_fkey" FOREIGN KEY ("kecamatan_id") REFERENCES "public"."kecamatan" ("kecamatan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_bps" ADD CONSTRAINT "master_bps_kelurahan_id_fkey" FOREIGN KEY ("kelurahan_id") REFERENCES "public"."kelurahan" ("kelurahan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_bps" ADD CONSTRAINT "master_bps_provinsi_id_fkey" FOREIGN KEY ("provinsi_id") REFERENCES "public"."provinsi" ("provinsi_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_kps
-- ----------------------------
ALTER TABLE "public"."master_kps" ADD CONSTRAINT "master_kps_bps_id_fkey" FOREIGN KEY ("bps_id") REFERENCES "public"."master_bps" ("bps_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_kriteria
-- ----------------------------
ALTER TABLE "public"."master_kriteria" ADD CONSTRAINT "master_kriteria_kriteria_id_parent_fkey" FOREIGN KEY ("kriteria_id_parent") REFERENCES "public"."master_kriteria" ("kriteria_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_kriteria" ADD CONSTRAINT "master_kriteria_tipe_kriteria_fkey" FOREIGN KEY ("tipe_kriteria") REFERENCES "public"."master_kriteria_tipe" ("tipe_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_kriteria_kategori
-- ----------------------------
ALTER TABLE "public"."master_kriteria_kategori" ADD CONSTRAINT "master_kriteria_kategori_tipe_kriteria_fkey" FOREIGN KEY ("tipe_kriteria") REFERENCES "public"."master_kriteria_tipe" ("tipe_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_pemda
-- ----------------------------
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_bps_id_fkey" FOREIGN KEY ("bps_id") REFERENCES "public"."master_bps" ("bps_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_kab_kota_id_fkey" FOREIGN KEY ("kab_kota_id") REFERENCES "public"."kabupaten" ("kabupaten_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_kecamatan_id_fkey" FOREIGN KEY ("kecamatan_id") REFERENCES "public"."kecamatan" ("kecamatan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_kelurahan_id_fkey" FOREIGN KEY ("kelurahan_id") REFERENCES "public"."kelurahan" ("kelurahan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pemda" ADD CONSTRAINT "master_pemda_provinsi_id_fkey" FOREIGN KEY ("provinsi_id") REFERENCES "public"."provinsi" ("provinsi_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table master_pendamping
-- ----------------------------
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_kab_kota_id_fkey" FOREIGN KEY ("kab_kota_id") REFERENCES "public"."kabupaten" ("kabupaten_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_kecamatan_id_fkey" FOREIGN KEY ("kecamatan_id") REFERENCES "public"."kecamatan" ("kecamatan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_kelurahan_id_fkey" FOREIGN KEY ("kelurahan_id") REFERENCES "public"."kelurahan" ("kelurahan_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_provinsi_id_fkey" FOREIGN KEY ("provinsi_id") REFERENCES "public"."provinsi" ("provinsi_id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."master_pendamping" ADD CONSTRAINT "master_pendamping_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table pemantauan
-- ----------------------------
ALTER TABLE "public"."pemantauan" ADD CONSTRAINT "pemantauan_pemantauan_petugas_fkey" FOREIGN KEY ("pemantauan_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table pendampingan
-- ----------------------------
ALTER TABLE "public"."pendampingan" ADD CONSTRAINT "pendampingan_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table pengawasan
-- ----------------------------
ALTER TABLE "public"."pengawasan" ADD CONSTRAINT "pengawasan_pengawasan_petugas_fkey" FOREIGN KEY ("pengawasan_petugas") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table pesan_kps
-- ----------------------------
ALTER TABLE "public"."pesan_kps" ADD CONSTRAINT "pesan_kps_kps_id_fkey" FOREIGN KEY ("kps_id") REFERENCES "public"."master_kps" ("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "public"."pesan_kps" ADD CONSTRAINT "pesan_kps_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table publikasi
-- ----------------------------
ALTER TABLE "public"."publikasi" ADD CONSTRAINT "publikasi_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table riwayat
-- ----------------------------
ALTER TABLE "public"."riwayat" ADD CONSTRAINT "riwayat_riwayat_arsip_fkey" FOREIGN KEY ("riwayat_arsip") REFERENCES "public"."arsip" ("arsip_id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "public"."riwayat" ADD CONSTRAINT "riwayat_riwayat_user_fkey" FOREIGN KEY ("riwayat_user") REFERENCES "public"."users" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table role_permissions
-- ----------------------------
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "public"."permissions" ("permission_id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("role_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table sertifikat_pendamping
-- ----------------------------
ALTER TABLE "public"."sertifikat_pendamping" ADD CONSTRAINT "sertifikat_pendamping_pendamping_id_fkey" FOREIGN KEY ("pendamping_id") REFERENCES "public"."master_pendamping" ("pendamping_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table user_roles
-- ----------------------------
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("role_id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_bps_id_fkey" FOREIGN KEY ("bps_id") REFERENCES "public"."master_bps" ("bps_id") ON DELETE SET NULL ON UPDATE CASCADE;
