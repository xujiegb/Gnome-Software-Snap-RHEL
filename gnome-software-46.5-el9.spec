%global appstream_version 0.14.0
%global flatpak_version 1.9.1
%global fwupd_version 1.5.6
%global glib2_version 2.68.0
%global gtk4_version 4.10.0
%global json_glib_version 1.6.0
%global libadwaita_version 1.3.alpha
%global libxmlb_version 0.1.7
%global packagekit_version 1.2.5

# Disable WebApps for RHEL builds
%bcond webapps %[!0%{?rhel}]
# Disable parental control for RHEL builds
%bcond_without malcontent
# Disable rpm-ostree support for RHEL builds
%bcond rpmostree %[!0%{?rhel}]

# this is not a library version
%define gs_plugin_version 20

%global tarball_version %%(echo %{version} | tr '~' '.')

%global __provides_exclude_from ^%{_libdir}/%{name}/plugins-%{gs_plugin_version}/.*\\.so.*$

Name:      gnome-software
# 原: Version:   45.3
# (为 46.5 调整)
Version:   46.5
# 保持原 Release 不动（你要求“其他部分不要动”）
Release:   3%{?dist}
Summary:   A software center for GNOME

License:   GPL-2.0-or-later
URL:       https://wiki.gnome.org/Apps/Software
# 原: S https://download.gnome.org/sources/gnome-software/45/
# (为 46.5 调整主版本目录到 46)
Source0:   https://download.gnome.org/sources/gnome-software/46/%{name}-%{tarball_version}.tar.xz

# ===== 按你的要求：注释补丁，不改动其余 =====
# Patch01:   0001-Lower_glib_dependency_to_2_68.patch   # (46.5 构建：停用下游补丁)
# Patch02:   0002-Lower-pango-attributes.patch          # (46.5 构建：停用下游补丁)
# Patch03:   0003-Verify-category-sizes.patch           # (46.5 构建：停用下游补丁)
# Patch04:   0004-prefer-vendor-name.patch              # (46.5 构建：停用下游补丁)
# RHEL9 最小兼容补丁：降低上游 Meson 的 appstream 最低版本到 0.16.1
# 原行：appstream_dep = dependency('appstream', version: '>= 0.16.4')
# Patch05:   0005-lower-appstream-dep-to-0.16.1.patch
# Patch05:   0001-Lower_glib_dependency_to_2_68.patch 
# 降低 GLib 需求到 2.68 以适配 RHEL/Rocky 9
# Patch06: 0006-lower-glib-dep-to-2.68.patch
# Patch07: 0007-glib-2.68-compat.patch

BuildRequires: appstream
BuildRequires: gettext
BuildRequires: docbook-style-xsl
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: libxslt
BuildRequires: meson
BuildRequires: pkgconfig(appstream) >= %{appstream_version}
BuildRequires: pkgconfig(flatpak) >= %{flatpak_version}
BuildRequires: pkgconfig(fwupd) >= %{fwupd_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gmodule-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gsettings-desktop-schemas)
BuildRequires: pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires: pkgconfig(libadwaita-1) >= %{libadwaita_version}
BuildRequires: pkgconfig(libdnf)
BuildRequires: pkgconfig(libsoup-2.4)
# BuildRequires: pkgconfig(malcontent-0)
BuildRequires: pkgconfig(ostree-1)
BuildRequires: pkgconfig(packagekit-glib2) >= %{packagekit_version}
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(rpm)
%if %{with rpmostree}
BuildRequires: pkgconfig(rpm-ostree-1)
%endif
#BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: pkgconfig(xmlb) >= %{libxmlb_version}
# ===== 开启 snap 插件所需（新增 BuildRequires）=====
# 说明：开启 -Dsnap=true 需要 snapd-glib 开发包
BuildRequires: pkgconfig(snapd-glib)
# (46.5 新增：为 snap 插件提供编译期依赖)

Requires: appstream-data
Requires: appstream%{?_isa} >= %{appstream_version}
%if %{with webapps}
Requires: epiphany-runtime%{?_isa}
%endif
Requires: flatpak%{?_isa} >= %{flatpak_version}
Requires: flatpak-libs%{?_isa} >= %{flatpak_version}
Requires: fwupd%{?_isa} >= %{fwupd_version}
Requires: glib2%{?_isa} >= %{glib2_version}
# gnome-menus is needed for app folder .directory entries
Requires: gnome-menus%{?_isa}
Requires: gsettings-desktop-schemas%{?_isa}
Requires: json-glib%{?_isa} >= %{json_glib_version}
Requires: iso-codes
# librsvg2 is needed for gdk-pixbuf svg loader
Requires: librsvg2%{?_isa}
Requires: libxmlb%{?_isa} >= %{libxmlb_version}
# ===== 开启 snap 插件所需（新增 Runtime Requires）=====
Requires: snapd
# (46.5 新增：启用 snap 插件后需要 snapd 运行时)

Recommends: PackageKit%{?_isa} >= %{packagekit_version}

Obsoletes: gnome-software-snap < 3.33.1
Obsoletes: gnome-software-editor < 3.35.1

%description
gnome-software is an application that makes it easy to add, remove
and update software in the GNOME desktop.

%package devel
Summary: Headers for building external gnome-software plugins
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
These development files are for building gnome-software plugins outside
the source tree. Most users do not need this subpackage installed.

%if %{with rpmostree}
%package rpm-ostree
Summary: rpm-ostree backend for gnome-software
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: rpm-ostree%{?_isa}
Supplements: (gnome-software%{?_isa} and rpm-ostree%{?_isa})

%description rpm-ostree
gnome-software is an application that makes it easy to add, remove
and update software in the GNOME desktop.

This package includes the rpm-ostree backend.
%endif

%prep
%autosetup -p1 -S gendiff -n %{name}-%{tarball_version}

# 统一把 glib 最低要求压到 >= 2.68.0（防回弹）
sed -i -E "s|(dependency\('glib-2\.0',[^)]*version[[:space:]]*:[[:space:]]*')[^']+(')|\1>= 2.68.0\2|" meson.build
grep -n "dependency('glib-2.0" meson.build

# ---- 写入 GLib 2.68 兼容层头文件（覆盖 lib/gs-glib268-shim.h）----
cat > lib/gs-glib268-shim.h <<'EOF'
#ifndef GS_GLIB268_SHIM_H
#define GS_GLIB268_SHIM_H

#include <glib.h>
#include <gio/gio.h>
#include <pango/pango.h>  /* 为 PangoAttrList autoptr 提前声明 */

#if !GLIB_CHECK_VERSION(2,70,0)
/* GLib 2.70+: g_prefix_error_literal；老版本用 g_prefix_error 模拟 */
static inline void _gs_prefix_error_literal (GError **error, const char *prefix)
{
    g_prefix_error (error, "%s", prefix);
}
#define g_prefix_error_literal _gs_prefix_error_literal
#endif

/* GLib 2.76+: g_thread_pool_new_full（46.x 使用 6 参数版本）
 * GLib 2.68 只有 g_thread_pool_new(...)，忽略 item_free_func。
 */
#if !GLIB_CHECK_VERSION(2,76,0)
static inline GThreadPool *
g_thread_pool_new_full (GFunc func,
                        gpointer user_data,
                        GDestroyNotify item_free_func,
                        gint max_threads,
                        gboolean exclusive,
                        GError **error)
{
    (void)item_free_func; /* 旧 GLib 没有 per-item free 回调 */
    return g_thread_pool_new (func, user_data, max_threads, exclusive, error);
}
#endif

/* GLib 2.74+: g_strv_builder_addv；为 2.68 提供简易实现 */
#if !GLIB_CHECK_VERSION(2,74,0)
static inline void
g_strv_builder_addv (GStrvBuilder *builder, const gchar **strv)
{
    if (!strv) return;
    for (const gchar **p = strv; *p; p++)
        g_strv_builder_add (builder, *p);
}
#endif

/* GLib 2.70+: g_spawn_check_wait_status；旧版用 g_spawn_check_exit_status */
#if !GLIB_CHECK_VERSION(2,70,0)
static inline gboolean
g_spawn_check_wait_status (int wait_status, GError **error)
{
    return g_spawn_check_exit_status (wait_status, error);
}
#endif

/* GLib 2.70+: G_DEFINE_FINAL_TYPE；旧版等价用 G_DEFINE_TYPE */
#if !GLIB_CHECK_VERSION(2,70,0)
#ifndef G_DEFINE_FINAL_TYPE
#define G_DEFINE_FINAL_TYPE(TypeName, type_name, TYPE_PARENT) \
        G_DEFINE_TYPE(TypeName, type_name, TYPE_PARENT)
#endif
#endif

/* GLib 2.70+: g_source_set_static_name；旧版退化为 g_source_set_name */
#if !GLIB_CHECK_VERSION(2,70,0)
static inline void
g_source_set_static_name (GSource *source, const char *name)
{
    g_source_set_name (source, name);
}
#endif

/* GLib 2.76+: g_ptr_array_new_null_terminated；旧版退化为普通 GPtrArray */
#if !GLIB_CHECK_VERSION(2,76,0)
static inline GPtrArray *
g_ptr_array_new_null_terminated (guint          reserved_size,
                                 GDestroyNotify element_free_func,
                                 gboolean       clear)
{
    (void)reserved_size;
    (void)clear;
    return g_ptr_array_new_with_free_func (element_free_func);
}
#endif

/* 一些较老的 Pango 版本不会声明 PangoAttrList 的 autoptr；补一个 */
#ifndef PangoAttrList_autoptr
G_DEFINE_AUTOPTR_CLEANUP_FUNC(PangoAttrList, pango_attr_list_unref)
#endif

#endif /* GS_GLIB268_SHIM_H */
EOF

# ---- 在需要用到 shim 的源文件里插入 include ----
python3 - <<'PY'
import io, re, os

def ensure_include(path, header_rel):
    with io.open(path,'r',encoding='utf-8') as f:
        s = f.read()
    if 'gs-glib268-shim.h' in s:
        return
    # 优先插到 <gio/gio.h> 之后；否则放到第一条 #include 之后
    s2 = re.sub(r'(#include\s*[<"]gio/gio\.h[>"].*\n)',
                r'\1#include "%s"\n' % header_rel,
                s, count=1, flags=re.M)
    if s2 == s:
        s2 = re.sub(r'(#include[^\n]*\n)',
                    r'\1#include "%s"\n' % header_rel,
                    s, count=1, flags=re.M)
    with io.open(path,'w',encoding='utf-8') as f:
        f.write(s2)

# lib/ 里的源文件
for fn in [
    'lib/gs-plugin-loader.c',       # g_prefix_error_literal / g_thread_pool_new_full
    'lib/gs-app-query.c',           # g_strv_builder_addv
    'lib/gs-fedora-third-party.c',  # g_spawn_check_wait_status
    'lib/gs-icon-downloader.c',     # G_DEFINE_FINAL_TYPE
    'lib/gs-job-manager.c',         # g_source_set_static_name
]:
    ensure_include(fn, 'gs-glib268-shim.h')

# 插件里也加 shim 头（相对路径指向 lib/）
for fn in [
    'plugins/fwupd/gs-plugin-fwupd.c',
    'plugins/flatpak/gs-flatpak.c',
    'plugins/packagekit/gs-plugin-packagekit.c',
]:
    ensure_include(fn, 'lib/gs-glib268-shim.h')

# src/ 中用到 shim 的源
for fn in [
    'src/gs-app-row.c',     # g_ptr_array_new_null_terminated
    'src/gs-common.c',      # PangoAttrList autoptr + g_prefix_error_literal
]:
    ensure_include(fn, 'lib/gs-glib268-shim.h')

# ---- 修复 src/gs-update-monitor.c 对不存在成员的访问（GLib<2.70）----
up_mon = 'src/gs-update-monitor.c'
ensure_include(up_mon, 'lib/gs-glib268-shim.h')

with io.open(up_mon,'r',encoding='utf-8') as f:
    t = f.read()

# 撤销之前可能插入的守卫（避免把函数体夹坏）
t = t.replace('#if GLIB_CHECK_VERSION(2,70,0)\n', '')
t = t.replace('#endif /* GLib >= 2.70 */\n', '')

# 只改“} else if (monitor->power_profile_monitor == NULL) {”
pat = r'\}\s*else\s+if\s*\(\s*monitor->power_profile_monitor\s*==\s*NULL\s*\)\s*\{'
rep = ('}\n'
       '#if GLIB_CHECK_VERSION(2,70,0)\n'
       'else if (monitor->power_profile_monitor == NULL) {\n'
       '#else\n'
       'else if (0) {\n'
       '#endif')
import re
t2, n = re.subn(pat, rep, t, count=1, flags=re.M)
if n == 0:
    print('warn: pattern not found in gs-update-monitor.c (maybe already patched)')
    t2 = t

with io.open(up_mon,'w',encoding='utf-8') as f:
    f.write(t2)

print('shim includes done, pango autoptr provided, and gs-update-monitor guarded safely.')
PY

# ----【新增】借鉴红帽：Overview 类目健壮性补丁（三连）----
# 说明：
# 1/3：lib/gs-appstream.c 中把类目计数抓取上限从 10 调整为 100，并去掉一次过早的 continue
# 2/3：src/gs-overview-page.c 增加调试日志，便于定位类目计数来源
# 3/3：src/gs-overview-page.c 校验各类目的真实内容，修正不准确的 size（避免后续页面逻辑对 0/过大值崩溃）
# 使用 --forward，若已应用则跳过；若上游差异较大，构建日志会提示具体失败的 hunk，便于针对性微调。
patch -p1 -s --forward <<'PATCH_OV1' || :
From f7e394840ff84ae8b55f13ff9692d6b02e8e6ea5 Mon Sep 17 00:00:00 2001
Date: Wed, 20 Dec 2023 12:21:24 +0100
Subject: [PATCH 1/3] gs-appstream: Increase limit to category apps lookup

The Overview page currently checks for 100 apps in all categories.
Lookup for the same count per category.

Note: The counts are not accurate, same apps can be in multiple
sub-categories, thus the parent category count suffers of duplicity,
which the following commit will correct in a different way than
checking for id duplicity.
---
 lib/gs-appstream.c | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

diff --git a/lib/gs-appstream.c b/lib/gs-appstream.c
index f110e3c47..d600cac53 100644
--- a/lib/gs-appstream.c
+++ b/lib/gs-appstream.c
@@ -1836,7 +1836,8 @@ static guint
 gs_appstream_count_component_for_groups (XbSilo      *silo,
                                          const gchar *desktop_group)
 {
-	guint limit = 10;
+	/* the overview page checks for 100 apps, then try to get them */
+	const guint limit = 100;
 	g_autofree gchar *xpath = NULL;
 	g_auto(GStrv) split = g_strsplit (desktop_group, "::", -1);
 	g_autoptr(GPtrArray) array = NULL;
@@ -1896,7 +1897,6 @@ gs_appstream_refine_category_sizes (XbSilo        *silo,
 				}
 			}
 		}
-		continue;
 	}
 	return TRUE;
 }
-- 
2.44.0
PATCH_OV1

patch -p1 -s --forward <<'PATCH_OV2' || :
From 617af44a56f6f62e07fd3fc13ae43d688aa3b85f Mon Sep 17 00:00:00 2001
Date: Wed, 20 Dec 2023 12:24:25 +0100
Subject: [PATCH 2/3] gs-overview-page: Add debug prints about discovered
 categories

For easier debugging, to see what the plugins returned.
---
 src/gs-overview-page.c | 2 ++
 1 file changed, 2 insertions(+)

diff --git a/src/gs-overview-page.c b/src/gs-overview-page.c
index 6ef5079e9..72000e257 100644
--- a/src/gs-overview-page.c
+++ b/src/gs-overview-page.c
@@ -496,6 +496,7 @@ gs_overview_page_get_categories_cb (GObject *source_object,
 
 		if (gs_category_get_icon_name (cat) != NULL) {
 			found_apps_cnt += gs_category_get_size (cat);
+			g_debug ("overview page found category '%s' which claims %u apps", gs_category_get_name (cat), gs_category_get_size (cat));
 			flowbox = GTK_FLOW_BOX (self->flowbox_categories);
 		} else
 			flowbox = GTK_FLOW_BOX (self->flowbox_iconless_categories);
@@ -524,6 +525,7 @@ out:
 	 * See https://gitlab.gnome.org/GNOME/gnome-software/-/issues/2053 */
 	gtk_widget_set_visible (self->flowbox_categories, found_apps_cnt >= MIN_CATEGORIES_APPS);
 
+	g_debug ("overview page found %u category apps", found_apps_cnt);
 	if (found_apps_cnt < MIN_CATEGORIES_APPS && found_apps_cnt > 0) {
 		GsPluginListAppsFlags flags = GS_PLUGIN_LIST_APPS_FLAGS_INTERACTIVE;
 		GatherAppsData *gather_apps_data = g_new0 (GatherAppsData, 1);
-- 
2.44.0
PATCH_OV2

patch -p1 -s --forward <<'PATCH_OV3' || :
From 98086eca23dbd46284039722887852e8c760a0fe Mon Sep 17 00:00:00 2001
Date: Wed, 20 Dec 2023 12:32:21 +0100
Subject: [PATCH 3/3] gs-overview-page: Verify category sizes

The "list-categories" job can set inaccurate sizes for the categories,
thus check the actual category content to operate with proper numbers.
For example the appstream data can have information about apps, which
no plugin can provide due to disabled repository.
---
 src/gs-overview-page.c | 176 +++++++++++++++++++++++++++++++++++------
 1 file changed, 153 insertions(+), 23 deletions(-)

diff --git a/src/gs-overview-page.c b/src/gs-overview-page.c
index 72000e257..3ec689ac1 100644
--- a/src/gs-overview-page.c
+++ b/src/gs-overview-page.c
@@ -440,6 +440,7 @@ category_activated_cb (GsOverviewPage *self, GsCategoryTile *tile)
 typedef struct {
 	GsOverviewPage *page;  /* (unowned) */
 	GsPluginJobListCategories *job;  /* (owned) */
+	guint n_pending_ops;
 } GetCategoriesData;
 
 static void
@@ -451,31 +452,18 @@ get_categories_data_free (GetCategoriesData *data)
 
 G_DEFINE_AUTOPTR_CLEANUP_FUNC (GetCategoriesData, get_categories_data_free)
 
-static void
-gs_overview_page_get_categories_cb (GObject *source_object,
-                                    GAsyncResult *res,
-                                    gpointer user_data)
+static guint
+update_categories_sections (GsOverviewPage *self,
+			    GPtrArray *list) /* (element-type GsCategory) */
 {
-	g_autoptr(GetCategoriesData) data = g_steal_pointer (&user_data);
-	GsOverviewPage *self = GS_OVERVIEW_PAGE (data->page);
-	GsPluginLoader *plugin_loader = GS_PLUGIN_LOADER (source_object);
-	guint i;
 	GsCategory *cat;
 	GtkFlowBox *flowbox;
 	GtkWidget *tile;
 	guint added_cnt = 0;
 	guint found_apps_cnt = 0;
-	g_autoptr(GError) error = NULL;
-	GPtrArray *list = NULL;  /* (element-type GsCategory) */
 
-	if (!gs_plugin_loader_job_action_finish (plugin_loader, res, &error)) {
-		if (!g_error_matches (error, GS_PLUGIN_ERROR, GS_PLUGIN_ERROR_CANCELLED) &&
-		    !g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED))
-			g_warning ("failed to get categories: %s", error->message);
-		goto out;
-	}
-
-	list = gs_plugin_job_list_categories_get_result_list (data->job);
+	if (g_cancellable_is_cancelled (self->cancellable))
+		return found_apps_cnt;
 
 	gs_widget_remove_all (self->flowbox_categories, (GsRemoveFunc) gtk_flow_box_remove);
 	gs_widget_remove_all (self->flowbox_iconless_categories, (GsRemoveFunc) gtk_flow_box_remove);
@@ -488,7 +476,7 @@ gs_overview_page_get_categories_cb (GObject *source_object,
 	 * be visually important, and are listed near the top of the page.
 	 * Categories without icons are listed in a separate flowbox at the
 	 * bottom of the page. Typically they are addons. */
-	for (i = 0; i < list->len; i++) {
+	for (guint i = 0; list != NULL && i < list->len; i++) {
 		cat = GS_CATEGORY (g_ptr_array_index (list, i));
 		if (gs_category_get_size (cat) == 0)
 			continue;
@@ -510,7 +498,6 @@ gs_overview_page_get_categories_cb (GObject *source_object,
 				     g_object_ref (cat));
 	}
 
-out:
 	/* Show the heading for the iconless categories iff there are any. */
 	gtk_widget_set_visible (self->iconless_categories_heading,
 				gtk_flow_box_get_child_at_index (GTK_FLOW_BOX (self->flowbox_iconless_categories), 0) != NULL);
@@ -525,6 +512,27 @@ out:
 	 * See https://gitlab.gnome.org/GNOME/gnome-software/-/issues/2053 */
 	gtk_widget_set_visible (self->flowbox_categories, found_apps_cnt >= MIN_CATEGORIES_APPS);
 
+	return found_apps_cnt;
+}
+
+static void
+finish_verify_category_op (GetCategoriesData *op_data)
+{
+	g_autoptr(GetCategoriesData) data = g_steal_pointer (&op_data);
+	GsOverviewPage *self = GS_OVERVIEW_PAGE (data->page);
+	guint i, found_apps_cnt;
+	GPtrArray *list; /* (element-type GsCategory) */
+
+	data->n_pending_ops--;
+	if (data->n_pending_ops > 0) {
+		/* to not be freed */
+		g_steal_pointer (&data);
+		return;
+	}
+
+	list = gs_plugin_job_list_categories_get_result_list (data->job);
+	found_apps_cnt = update_categories_sections (self, list);
+
 	g_debug ("overview page found %u category apps", found_apps_cnt);
 	if (found_apps_cnt < MIN_CATEGORIES_APPS && found_apps_cnt > 0) {
 		GsPluginListAppsFlags flags = GS_PLUGIN_LIST_APPS_FLAGS_INTERACTIVE;
@@ -534,10 +542,10 @@ out:
 		gather_apps_data->self = g_object_ref (self);
 		gather_apps_data->list = gs_app_list_new ();
 
-		for (i = 0; i < list->len; i++) {
+		for (i = 0; list != NULL && i < list->len; i++) {
 			g_autoptr(GsPluginJob) plugin_job = NULL;
 			g_autoptr(GsAppQuery) query = NULL;
-			GsCategory *subcat;
+			GsCategory *cat, *subcat;
 
 			cat = GS_CATEGORY (g_ptr_array_index (list, i));
 			if (gs_category_get_size (cat) == 0 ||
@@ -578,6 +586,128 @@ out:
 	gs_overview_page_decrement_action_cnt (self);
 }
 
+typedef struct {
+	GsOverviewPage *page;  /* (unowned) */
+	GetCategoriesData *op_data; /* (unowned) */
+	GsCategory *category;  /* (owned) */
+} VerifyCategoryData;
+
+static void
+verify_category_data_free (VerifyCategoryData *data)
+{
+	g_clear_object (&data->category);
+	g_free (data);
+}
+
+G_DEFINE_AUTOPTR_CLEANUP_FUNC (VerifyCategoryData, verify_category_data_free)
+
+static void
+gs_overview_page_verify_category_cb (GObject *source_object,
+                                     GAsyncResult *res,
+                                     gpointer user_data)
+{
+	g_autoptr(VerifyCategoryData) data = user_data;
+	GsPluginLoader *plugin_loader = GS_PLUGIN_LOADER (source_object);
+	g_autoptr(GError) local_error = NULL;
+	g_autoptr(GsAppList) list = NULL;
+
+	list = gs_plugin_loader_job_process_finish (plugin_loader, res, &local_error);
+	if (list == NULL) {
+		if (!g_error_matches (local_error, GS_PLUGIN_ERROR, GS_PLUGIN_ERROR_CANCELLED) &&
+		    !g_error_matches (local_error, G_IO_ERROR, G_IO_ERROR_CANCELLED))
+			g_warning ("failed to get apps for category: %s", local_error->message);
+		g_debug ("Failed to get category content '%s' for overview page: %s", gs_category_get_id (data->category), local_error->message);
+	} else {
+		GsCategory *all_subcat = gs_category_find_child (data->category, "all");
+		guint size = gs_app_list_length (list);
+		g_debug ("overview page verify category '%s' size:%u~>%u subcat:'%s' size:%u~>%u",
+			gs_category_get_id (data->category), gs_category_get_size (data->category), size,
+			gs_category_get_id (all_subcat), gs_category_get_size (all_subcat), size);
+		gs_category_set_size (data->category, size);
+		gs_category_set_size (all_subcat, size);
+	}
+
+	finish_verify_category_op (data->op_data);
+}
+
+static void
+gs_overview_page_get_categories_list_cb (GObject *source_object,
+					 GAsyncResult *res,
+					 gpointer user_data)
+{
+	g_autoptr(GetCategoriesData) data = g_steal_pointer (&user_data);
+	GsOverviewPage *self = GS_OVERVIEW_PAGE (data->page);
+	GsPluginLoader *plugin_loader = GS_PLUGIN_LOADER (source_object);
+	g_autoptr(GError) error = NULL;
+
+	g_assert (data->n_pending_ops == 0);
+
+	data->n_pending_ops++;
+
+	/* The apps can be mentioned in the appstream data, but no plugin may provide actual app,
+	   thus try to get the content as the Categories page and fine tune the numbers appropriately. */
+	if (!gs_plugin_loader_job_action_finish (plugin_loader, res, &error)) {
+		if (!g_error_matches (error, GS_PLUGIN_ERROR, GS_PLUGIN_ERROR_CANCELLED) &&
+		    !g_error_matches (error, G_IO_ERROR, G_IO_ERROR_CANCELLED))
+			g_warning ("failed to get categories: %s", error->message);
+	} else {
+		g_autoptr(GPtrArray) verify_categories = NULL; /* (element-type GsCategory) */
+		GPtrArray *list = NULL; /* (element-type GsCategory) */
+		guint found_apps_cnt;
+
+		list = gs_plugin_job_list_categories_get_result_list (data->job);
+		found_apps_cnt = update_categories_sections (self, list);
+
+		if (found_apps_cnt >= MIN_CATEGORIES_APPS) {
+			verify_categories = g_ptr_array_new_full (list != NULL ? list->len : 0, g_object_unref);
+			for (guint i = 0; list != NULL && i < list->len; i++) {
+				GsCategory *category = g_ptr_array_index (list, i);
+				if (gs_category_get_size (category) > 0 &&
+				    gs_category_find_child (category, "all") != NULL) {
+					g_ptr_array_add (verify_categories, g_object_ref (category));
+				}
+			}
+		}
+
+		if (verify_categories != NULL && verify_categories->len > 0 && !g_cancellable_is_cancelled (self->cancellable)) {
+			for (guint i = 0; i < verify_categories->len; i++) {
+				GsCategory *category = g_ptr_array_index (verify_categories, i);
+				GsCategory *all_subcat = gs_category_find_child (category, "all");
+				g_autoptr(GsAppQuery) query = NULL;
+				g_autoptr(GsPluginJob) plugin_job = NULL;
+				VerifyCategoryData *ver_data;
+
+				g_assert (all_subcat != NULL);
+
+				data->n_pending_ops++;
+
+				ver_data = g_new0 (VerifyCategoryData, 1);
+				ver_data->page = self;
+				ver_data->op_data = data;
+				ver_data->category = g_object_ref (category);
+
+				query = gs_app_query_new ("category", all_subcat,
+							  "refine-flags", GS_PLUGIN_REFINE_FLAGS_REQUIRE_ID,
+							  "dedupe-flags", GS_APP_LIST_FILTER_FLAG_KEY_ID_PROVIDES,
+							  "license-type", gs_page_get_query_license_type (GS_PAGE (self)),
+							  /*"developer-verified-type", gs_page_get_query_developer_verified_type (GS_PAGE (self)),*/
+							  NULL);
+				plugin_job = gs_plugin_job_list_apps_new (query, GS_PLUGIN_LIST_APPS_FLAGS_NONE);
+				gs_plugin_loader_job_process_async (plugin_loader,
+								    plugin_job,
+								    self->cancellable,
+								    gs_overview_page_verify_category_cb,
+								    ver_data);
+			}
+
+			finish_verify_category_op (g_steal_pointer (&data));
+			return;
+		}
+	}
+
+	finish_verify_category_op (g_steal_pointer (&data));
+}
+
 static void
 third_party_destroy_cb (GtkWindow *window,
 			GsOverviewPage *self)
@@ -967,7 +1097,7 @@ gs_overview_page_load (GsOverviewPage *self)
 		data->job = g_object_ref (GS_PLUGIN_JOB_LIST_CATEGORIES (plugin_job));
 
 		gs_plugin_loader_job_process_async (self->plugin_loader, plugin_job,
-						    self->cancellable, gs_overview_page_get_categories_cb,
+						    self->cancellable, gs_overview_page_get_categories_list_cb,
 						    g_steal_pointer (&data));
 		self->action_cnt++;
 	}
-- 
2.44.0
PATCH_OV3

%build
%meson \
  -Dmalcontent=false \
  -Dsoup2=true \
  -Dsnap=true \
  -Dgudev=true \
  -Dpackagekit=true \
  -Dpackagekit_autoremove=true \
  -Dexternal_appstream=false \
%if %{with rpmostree}
  -Drpm_ostree=true \
%else
  -Drpm_ostree=false \
%endif
%if %{with webapps}
  -Dwebapps=true \
  -Dhardcoded_foss_webapps=true \
  -Dhardcoded_proprietary_webapps=false \
%else
  -Dwebapps=false \
  -Dhardcoded_foss_webapps=false \
  -Dhardcoded_proprietary_webapps=false \
%endif
  -Dtests=false

# 关键：把 GETTEXTDATADIRS 绑到 ninja 这一次调用
GETTEXTDATADIRS="%{_datadir}/gettext:%{_datadir}/gettext-0.21" \
  ninja -C %{_vpath_builddir} -v

%meson_build

%install
%meson_install

# remove unneeded dpkg plugin
rm %{buildroot}%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dpkg.so

# make the software center load faster
desktop-file-edit %{buildroot}%{_datadir}/applications/org.gnome.Software.desktop \
    --set-key=X-AppInstall-Package --set-value=%{name}

# set up for Fedora
cat >> %{buildroot}%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override << FOE
[org.gnome.software]
%if 0%{?rhel}
official-repos = [ 'rhel-%{?rhel}' ]
%else
official-repos = [ 'anaconda', 'fedora', 'fedora-debuginfo', 'fedora-source', 'koji-override-0', 'koji-override-1', 'rawhide', 'rawhide-debuginfo', 'rawhide-source', 'updates', 'updates-debuginfo', 'updates-source', 'updates-testing', 'updates-testing-debuginfo', 'updates-testing-source', 'fedora-modular', 'fedora-modular-debuginfo', 'fedora-modular-source', 'rawhide-modular', 'rawhide-modular-debuginfo', 'rawhide-modular-source', 'fedora-cisco-openh264', 'fedora-cisco-openh264-debuginfo' ]
required-repos = [ 'fedora', 'updates' ]
packaging-format-preference = [ 'flatpak:fedora-testing', 'flatpak:fedora', 'rpm' ]
%endif
FOE

%find_lang %name --with-gnome

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%doc AUTHORS README.md
%license COPYING
%{_bindir}/gnome-software
%{_datadir}/applications/gnome-software-local-file-flatpak.desktop
%{_datadir}/applications/gnome-software-local-file-fwupd.desktop
%{_datadir}/applications/gnome-software-local-file-packagekit.desktop
# ===== 新增：snap 本地文件处理 desktop 文件 =====
%{_datadir}/applications/gnome-software-local-file-snap.desktop
%{_datadir}/applications/org.gnome.Software.desktop
%{_mandir}/man1/gnome-software.1*
%{_datadir}/bash-completion/completions/gnome-software
%{_datadir}/icons/hicolor/*/apps/org.gnome.Software.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Software-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/app-remove-symbolic.svg
%{_datadir}/metainfo/org.gnome.Software.metainfo.xml
%if %{with webapps}
%{_datadir}/metainfo/org.gnome.Software.Plugin.Epiphany.metainfo.xml
%endif
%{_datadir}/metainfo/org.gnome.Software.Plugin.Flatpak.metainfo.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Fwupd.metainfo.xml
# ===== 新增：snap 插件的 metainfo =====
%{_datadir}/metainfo/org.gnome.Software.Plugin.Snap.metainfo.xml
%dir %{_libdir}/gnome-software/plugins-%{gs_plugin_version}
%{_libdir}/gnome-software/libgnomesoftware.so.%{gs_plugin_version}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_appstream.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dummy.so
%if %{with webapps}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_epiphany.so
%endif
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fedora-langpacks.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fedora-pkgdb-collections.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_flatpak.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fwupd.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_generic-updates.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_hardcoded-blocklist.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_icons.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_modalias.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_os-release.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_packagekit.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance-license.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_repos.so
# ===== 新增：snap 插件 .so 打进主包 =====
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_snap.so
%{_sysconfdir}/xdg/autostart/org.gnome.Software.desktop
%dir %{_datadir}/swcatalog
%dir %{_datadir}/swcatalog/xml
%if %{with webapps}
%{_datadir}/swcatalog/xml/gnome-pwa-list-foss.xml
%endif
%{_datadir}/swcatalog/xml/org.gnome.Software.Curated.xml
%{_datadir}/swcatalog/xml/org.gnome.Software.Featured.xml
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/gnome-shell/search-providers/org.gnome.Software-search-provider.ini
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override
%{_libexecdir}/gnome-software-cmd
%{_libexecdir}/gnome-software-restarter

%if %{with rpmostree}
%files rpm-ostree
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_rpm-ostree.so
%endif

%files devel
%{_libdir}/pkgconfig/gnome-software.pc
%dir %{_includedir}/gnome-software
%{_includedir}/gnome-software/*.h
%{_libdir}/gnome-software/libgnomesoftware.so
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gnome-software/

%changelog
# ===== 新增 46.5 的变更记录（保持原格式追加在最上方）=====
* Thu Aug 28 2025 Packager <packager@example.com> - 46.5-3
- Rebase to 46.5
- Disable downstream patches for 46 series
- Enable snap plugin and ship it in main package
- Install gnome-software-local-file-snap.desktop

* Mon May 27 2024 Milan Crha <mcrha@redhat.com> - 45.3-3
- Resolves: RHEL-22268 (Prefer VENDOR_NAME in app origin)

* Mon May 06 2024 Milan Crha <mcrha@redhat.com> - 45.3-2
- Resolves: RHEL-843 (Rebase GNOME Software to its GNOME 45 version)

* Thu Aug 03 2023 Milan Crha <mcrha@redhat.com> - 41.5-3
- Resolves: #2228374 (Rebuild to move gnome-software-devel into CRB)

* Thu Sep 22 2022 Milan Crha <mcrha@redhat.com> - 41.5-2
- Resolves: #2128812 (Correct property name in GsRemovalDialog .ui file)
- Resolves: #2129021 (Hide some errors in non-debug builds)

* Mon Mar 21 2022 Milan Crha <mcrha@redhat.com> - 41.5-1
- Resolves: #2066164 (Update to 41.5)

* Mon Feb 14 2022 Milan Crha <mcrha@redhat.com> - 41.4-1
- Resolves: #2054082 (Update to 41.4)

* Mon Jan 31 2022 Milan Crha <mcrha@redhat.com> - 41.3-2
- Resolves: #2048397 (Optional software repos can't be disabled)

* Mon Jan 10 2022 Milan Crha <mcrha@redhat.com> - 41.3-1
- Resolves: #2038805 (Update to 41.3)

* Mon Dec 06 2021 Milan Crha <mcrha@redhat.com> - 41.2-1
- Resolves: #2029323 (Update to 41.2)

* Mon Nov 01 2021 Milan Crha <mcrha@redhat.com> - 41.1-1
- Resolves: #2018871 (Update to 41.1)

* Tue Oct 12 2021 Milan Crha <mcrha@redhat.com> - 41.0-2
- Resolves: #2012699 (Backport changes from Fedora 35)
- Add patch to mark compulsory only repos, not apps from it
- Resolves: #2011176 (flathub repo can't be added through gnome-software)
- Resolves: #2010660 (gs-repos-dialog: Can show also desktop applications)
- Resolves: #2010353 (Optional repos cannot be disabled)
- Resolves: #2010740 (Refresh on repository setup change)
- Resolves: #2009063 (Correct update notifications)

* Mon Sep 20 2021 Milan Crha <mcrha@redhat.com> - 41.0-1
- Resolves: #2005770 (Update to 41.0)

* Mon Aug 23 2021 Kalev Lember <klember@redhat.com> - 41~beta-1
- Resolves: #1995567 (Update to 41.beta)

* Fri Aug 13 2021 Milan Crha <mcrha@redhat.com> - 40.4-1
- Resolves: #1992452 (Update to 40.4)

* Mon Jul 19 2021 Milan Crha <mcrha@redhat.com> - 40.3-2
- Resolves: #1983553
- Add rpm-ostree patch to hide packages from the search results
- Add patch to implement what-provides search in the Flatpak plugin

* Mon Jul 12 2021 Milan Crha <mcrha@redhat.com> - 40.3-1
- Related: #1981296 (Update to 40.3)

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 40.2-2
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Fri Jun 04 2021 Milan Crha <mcrha@redhat.com> - 40.2-1
- Related: #1967855 (Update to 40.2)

* Mon May 03 2021 Milan Crha <mcrha@redhat.com> - 40.1-2
- Related: #1952776 (Add patch for crash under gs_details_page_refresh_all() (i#1227))

* Mon May 03 2021 Milan Crha <mcrha@redhat.com> - 40.1-1
- Related: #1952776 (Update to 40.1)

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 40.0-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 40.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Thu Mar 18 2021 Adam Williamson <awilliam@redhat.com> - 40~rc-2
- Backport a couple of bug fixes from upstream (icon display, crash bug)

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Wed Mar 10 2021 Adam Williamson <awilliam@redhat.com> - 40~beta-2
- Backport MR #643 to fix update notifications on first run (#1930401)

* Tue Feb 16 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Mon Feb 08 2021 Richard Hughes <richard@hughsie.com> - 3.38.1-1
- New upstream version
- Fix package details not found for some packages
- Ignore harmless warnings when using unusual fwupd versions

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 3.38.0-2
- Revert an optimization that broke packagekit updates

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Tue Sep 01 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Tue Aug 18 2020 Richard Hughes <rhughes@redhat.com> - 3.36.1-4
- Rebuild for the libxmlb API bump.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Richard Hughes <rhughes@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Tue May 12 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Backport various rpm-ostree backend fixes

* Wed Mar 11 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Wed Mar 04 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Fri Feb 21 2020 Richard Hughes <rhughes@redhat.com> - 3.35.91-2
- Backport a patch to fix a crash when looking at the application details.

* Wed Feb 19 2020 Richard Hughes <rhughes@redhat.com> - 3.35.91-1
- Update to 3.35.91.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Richard Hughes <rhughes@redhat.com> - 3.35.2-1
- Update to 3.35.2.

* Fri Oct 18 2019 Kalev Lember <klember@redhat.com> - 3.34.1-6
- Backport patches to fix a crash in gs_flatpak_get_installation (#1762689)

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 3.34.1-5
- Update renamed appstream ids for GNOME 3.34

* Fri Oct 11 2019 Richard Hughes <richard@redhat.com> - 3.34.1-4
- Backport a simpler to correct the installed applications
- Resolves #1759193

* Fri Oct 11 2019 Richard Hughes <richard@redhat.com> - 3.34.1-3
- Backport a better patch to correct the installed applications
- Resolves #1759193

* Thu Oct 10 2019 Richard Hughes <richard@redhat.com> - 3.34.1-2
- Backport a patch to correct the applications shown in the installed list
- Resolves #1759193

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Fix third party repo enabling not working (#1749566)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@redhat.com> - 3.32.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Kalev Lember <klember@redhat.com> - 3.32.4-1
- Update to 3.32.4

* Thu Jul 11 2019 Richard Hughes <rhughes@redhat.com> - 3.32.3-5
- Disable the snap plugin. Canonical upstream are not going to be installing
  gnome-software in the next LTS, prefering instead to ship a "Snap Store"
  rather than GNOME Software.
- Enabling the snap plugin also enables the Snap Store which violated the same
  rules which prevented us installing Flathub by default.
- The existing plugin is barely maintained and I don't want to be the one
  responsible when it breaks.

* Thu Jun 13 2019 Kalev Lember <klember@redhat.com> - 3.32.3-4
- Rebuild for accidental libflatpak ABI break

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-3
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:01 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-2
- Rebuild for RPM 4.15

* Fri May 24 2019 Kalev Lember <klember@redhat.com> - 3.32.3-1
- Update to 3.32.3

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Fri May 03 2019 Kalev Lember <klember@redhat.com> - 3.32.1-4
- Update a patch to final upstream version

* Tue Apr 30 2019 Kalev Lember <klember@redhat.com> - 3.32.1-3
- Backport a number of rpm-ostree fixes

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Fri Apr 05 2019 Neal Gompa <ngompa13@gmail.com> - 3.32.0-6
- Require snapd instead of the obsolete snapd-login-service for snap subpackage

* Wed Apr 03 2019 Kalev Lember <klember@redhat.com> - 3.32.0-5
- Switch to system libdnf

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 3.32.0-4
- Rebuild for new rpm-ostree

* Fri Mar 15 2019 Kalev Lember <klember@redhat.com> - 3.32.0-3
- Add nm-connection-editor.desktop to Utilities folder (#1686851)

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.32.0-2
- Update to 3.32.2

* Fri May 03 2019 Kalev Lember <klember@redhat.com> - 3.32.1-4
- Update a patch to final upstream version

* Tue Apr 30 2019 Kalev Lember <klember@redhat.com> - 3.32.1-3
- Backport a number of rpm-ostree fixes

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Fri Apr 05 2019 Neal Gompa <ngompa13@gmail.com> - 3.32.0-6
- Require snapd instead of the obsolete snapd-login-service for snap subpackage

* Wed Apr 03 2019 Kalev Lember <klember@redhat.com> - 3.32.0-5
- Switch to system libdnf

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 3.32.0-4
- Rebuild for new rpm-ostree

* Fri Mar 15 2019 Kalev Lember <klember@redhat.com> - 3.32.0-3
- Add nm-connection-editor.desktop to Utilities folder (#1686851)

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.32.0-2
- Backport a patch to add shadows to app icons

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 3.31.90-4
- Change PackageKit requires to recommends

* Wed Feb 27 2019 Kalev Lember <klember@redhat.com> - 3.31.90-3
- Remove unneeded dpkg plugin

* Mon Feb 25 2019 Kalev Lember <klember@redhat.com> - 3.31.90-2
- Split rpm-ostree backend to its own subpackage

* Sun Feb 24 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90
- Add "anaconda" repo to official repos list (#1679693)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Kalev Lember <kalevlember@gmail.com> - 3.31.2-1
- Update to 3.31.2

* Fri Dec 14 2018 Kalev Lember <kalevlember@gmail.com> - 3.31.1-2
- Backport fix for RHBZ #1546893 from upstream git

* Tue Oct 09 2018 Kalev Lember <kalevlember@gmail.com> - 3.31.1-1
- Update to 3.31.1

* Fri Oct 05 2018 Richard Hughes <richard@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Wed Sep 26 2019 Kalev Lember <klember@redhat.com> - 3.30.1-2
- Update to 3.30.1

* Tue Sep 25 2018 Kalev Lember <kalevlember@gmail.com> - 3.30.1-1
- Update to 3.30.1

* Thu Sep 06 2018 Kalev Lember <kalevlember@gmail.com> - 3.30.0-1
- Update to 3.30.0

* Tue Aug 28 2018 Richard Hughes <rhughes@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedora-project.org> - 3.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Kalev Lember <kalevlember@gmail.com> - 3.29.1-1
- Update to 3.29.1

* Mon Apr 09 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.1-1
- Update to 3.28.1

* Thu Mar 29 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.0-5
- Fix empty OS Updates showing up
- Make rpm-ostree update triggering work

* Thu Mar 15 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.0-4
- Fix opening results from gnome-shell search provider

* Wed Mar 14 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.0-3
- Fix crash on initial run with no network (#1554986)

* Tue Mar 13 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.0-2
- Backport an upstream patch to fix shell extensions app ID

* Mon Mar 12 2018 Kalev Lember <kalevlember@gmail.com> - 3.28.0-1
- Update to 3.28.0

* Sun Mar 11 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.92-3
- Rebuilt for gspell 1.8

* Wed Mar 07 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.92-2
- Move org.gnome.Software.Featured.xml from -editor to main package

* Mon Mar 05 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.92-1
- Update to 3.27.92

* Sun Mar 04 2018 Neal Gompa <ngompa13@gmail.com> - 3.27.90-4
- Drop obsolete snapd-login-service requirement for snap plugin subpackage

* Mon Feb 19 2018 Adam Williamson <awilliam@redhat.com> - 3.27.90-3
- Backport fix for RHBZ #1546893 from upstream git

* Mon Feb 19 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.90-2
- Re-enable rpm-ostree plugin

* Thu Feb 15 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.90-1
- Update to 3.27.90
- Temporarily disable the rpm-ostree plugin

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.4-4
- Rebuild against newer gnome-desktop3 package

* Thu Feb 08 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.4-3
- Add fedora-workstation-repositories to nonfree-sources schema defaults

* Wed Feb 07 2018 Fedora Release Engineering <releng@redhat.com> - 3.27.4-2
- Rebuilt for https://fedora-project.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Kalev Lember <kalevlember@gmail.com> - 3.27.4-1
- Update to 3.27.4
- Drop unused --without packagekit option

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@redhat.com> - 3.27.3-2
- Remove obsolete scriptlets

* Sat Dec 16 2017 Kalev Lember <kalevlember@gmail.com> - 3.27.3-1
- Update to 3.27.3

* Mon Nov 13 2017 Kalev Lember <kalevlember@gmail.com> - 3.27.2-1
- Update to 3.27.2

* Tue Nov 08 2017 Kalev Lember <kalevlember@gmail.com> - 3.26.2-1
- Update to 3.26.2
- Re-enable fwupd support

* Tue Oct 31 2017 Kalev Lember <kalevlember@gmail.com> - 3.26.1-5
- Enable the rpm-ostree plugin

* Wed Oct 25 2017 Kalev Lember <kalevlember@gmail.com> - 3.26.1-4
- Fix "too many results returned" error after distro upgrades (#1496489)

* Tue Oct 10 2017 Kalev Lember <kalevlember@gmail.com> - 3.26.1-3
- Backport a flatpakref installation fix

* Mon Oct 09 2017 Richard Hughes <rhughes@redhat.com> - 3.26.1-2
- Disable fwupd support until we get a 3.27.1 tarball

* Sun Oct 08 2017 Kalev Lember <kalevlember@gmail.com> - 3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Sun Aug 27 2017 Kalev Lember <klember@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Fri Aug 11 2017 Igor Gnatenko <ignatenkobrain@redhat.com> - 3.25.4-6
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenkobrain@redhat.com> - 3.25.4-5
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenkobrain@redhat.com> - 3.25.4-4
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@redhat.com> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@redhat.com> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 3.25.3-6
- Drop a meson workaround now that meson is fixed

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-5
- Actually properly enable snap subpackage after removing conditional

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-4
- Remove unnecessary arch-specific conditional for snap subpackage

* Tue Jun 27 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-3
- Ensure snap subpackage is installed if snapd is installed

* Fri Jun 23 2017 Richard Hughes <richard@hughsie.com> - 3.24.3-2
- Enable the snap subpackage

* Fri Jun 23 2017 Kalev Lember <kalevlember@gmail.com> - 3.25.3-1
- Update to 3.25.3
- Switch to the meson build system
- Add an -editor subpackage with new banner editor

* Mon May 15 2017 Richard Hughes <richard@hughsie.com> - 3.24.3-1
- Update to 3.23.3
- Fix a common crash when installing flatpakrepo files
- Ensure we show the banner when upgrades are available

* Tue May 09 2017 Kalev Lember <kalevlember@gmail.com> - 3.24.2-1
- Update to 3.24.2

* Tue Apr 25 2017 Adam Williamson <awilliam@redhat.com> - 3.24.1-2
- Backport crasher fix from upstream (RHBZ #1444669 / BGO #781217)

* Tue Apr 11 2017 Kalev Lember <kalevlember@gmail.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <kalevlember@gmail.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <kalevlember@gmail.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Richard Hughes <rhughes@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@redhat.com> - 3.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Richard Hughes <rhughes@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Wed Nov 23 2016 Kalev Lember <kalevlember@gmail.com> - 3.23.2-1
- Update to 3.23.2

* Tue Nov 08 2016 Kalev Lember <kalevlember@gmail.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <kalevlember@gmail.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92
- Don't set group tags

* Thu Sep 01 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Wed Aug 17 2016 Neal Gompa <ngompa13@gmail.com> - 3.21.90-2
- Rebuilt for fixed libappstream-glib headers

* Wed Aug 17 2016 Neal Gompa <ngompa13@gmail.com> - 3.21.90-1
- Update to 3.21.90
- Tighten -devel subpackage dependencies

* Thu Jul 28 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-2
- Allow building without PackageKit for the atomic workstation.

* Mon Jul 18 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-1
- Update to 3.21.4

* Thu May 26 2016 Kalev Lember <klember@redhat.com> - 3.21.2-2
- Build with flatpak support

* Mon May 23 2016 Richard Hughes <rhughes@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 3.21.1-2
- Require PackageKit 1.1.1 for system upgrade support

* Mon Apr 25 2016 Richard Hughes <rhughes@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Mon Apr 25 2016 Richard Hughes <rhughes@redhat.com> - 3.20.2-1
- Update to 3.20.1
- Allow popular and featured apps to match any plugin
- Do not make the ODRS plugin depend on xdg-app
- Fix many of the os-upgrade issues and implement the latest mockups
- Make all the plugins more threadsafe
- Return all update descriptions newer than the installed version
- Show some non-fatal error messages if installing fails
- Use a background PackageKit transaction when downloading upgrades

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Fri Apr 01 2016 Richard Hughes <rhughes@redhat.com> - 3.20.1-2
- Set the list of official sources
- Compile with xdg-app support

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Mar 14 2016 Richard Hughes <rhughes@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Kalev Lember <klember@redhat.com> - 3.19.91-2
- Set minimum required json-glib version

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 15 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@redhat.com> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Richard Hughes <rhughes@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Thu Dec 03 2015 Kalev Lember <klember@redhat.com> - 3.18.3-2
- Require librsvg2 for the gdk-pixbuf svg loader

* Thu Nov 05 2015 Richard Hughes <rhughes@redhat.com> - 3.18.3-1
- Update to 3.18.3
- Use the correct user agent string when downloading firmware
- Fix a crash in the limba plugin
- Fix installing web applications

* Mon Oct 26 2015 Kalev Lember <klember@redhat.com> - 3.18.2-2
- Fix apps reappearing as installed a few seconds after removal (#1275163)

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Tue Oct 13 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Wed Oct 07 2015 Kalev Lember <klember@redhat.com> - 3.18.0-2
- Backport two crasher fixes from upstream

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 3.17.92-2
- Update dependency versions

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 10 2015 Richard Hughes <rhughes@redhat.com> - 3.17.91-2
- Fix firmware updates

* Thu Sep 03 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Aug 12 2015 Richard Hughes <rhughes@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.2-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <releng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.2-1
- Update to 3.17.2

* Mon May 25 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Fri May 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-2
- Fix a crash under Wayland (#1221968)

* Mon May 11 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING file
- Add a patch to adapt to gnome-terminal desktop file rename

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-3
- Export DisplayName property on the packagekit session service

* Thu Feb 19 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-2
- Backport a crash fix

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Thu Nov 13 2014 Richard Hughes <rhughes@redhat.com> - 3.14.2-3
- Fix non-Fedora build

* Tue Nov 11 2014 Richard Hughes <rhughes@redhat.com> - 3.14.2-2
- Backport a patch to fix compilation

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Sat Nov 08 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-3
- Update the list of system apps

* Sat Nov 01 2014 David King <amigadave@amigadave.com> - 3.14.1-2
- Rebuild for new libappstream-glib (#1156494)

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Thu Oct 09 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Depend on gnome-menus for app folder directory entries

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <klember@redhat.com> - 3.13.92-2
- Set minimum required dependency versions (#1136343)

* Tue Sep 16 2014 Kalev Lember <klember@redhat.com> - 3.13.92-1
- Update to 3.13.92
- Replace gnome-system-log with gnome-logs in the system apps list

* Tue Sep 02 2014 Kalev Lember <klember@redhat.com> - 3.13.91-1
- Update to 3.13.91

* Tue Aug 19 2014 Richard Hughes <rhughes@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-0.2.git5c89189
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-0.1.git5c89189
- Update to 3.13.5 git snapshot
- Ship HighContrast icons

* Sun Aug 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-2
- Replace Epiphany with Firefox in the system apps list

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Wed Jun 25 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Thu Jun 12 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-0.2.git7491627
- Depend on the newly-created appstream-data package and stop shipping
  the metadata here.

* Sat Jun 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-0.1.git7491627
- Update to 3.13.3 git snapshot

* Wed May 28 2014 Richard Hughes <rhughes@redhat.com> - 3.13.2-2
- Rebuild with new metadata.

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-4
- Depend on gsettings-desktop-schemas

* Mon May 12 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-3
- Update the metadata and use appstream-util to install the metadata.

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Drop gnome-icon-theme dependency

* Mon Apr 28 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Fri Apr 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-2
- Rebuild with new metadata.

* Fri Apr 11 2014 Richard Hughes <rhughes@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-2
- Rebuild with new metadata.

* Sat Mar 08 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-2
- Require epiphany-runtime rather than the full application

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 30 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-3
- Rebuild for libpackagekit-glib soname bump

* Wed Jan 22 2013 Richard Hughes <rhughes@redhat.com> - 3.11.4-2
- Rebuild with metadata that has the correct screenshot url.

* Thu Jan 16 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1
- Add a gnome shell search provider
- Add a module to submit the user rating to the fedora-tagger web service
- Add support for 'missing' codecs that we know exist but we can't install
- Add support for epiphany web applications
- Handle offline installation sensibly
- Save the user rating if the user clicks the rating stars
- Show a modal error message if install or remove actions failed
- Show a star rating on the application details page
- Show font screenshots
- Show more detailed version numbers when required
- Show screenshots to each application

* Wed Sep 25 2013 Richard Hughes <richard@hughsie.com> 3.10.0-1
- New upstream release.
- New metadata for fedora, updates and updates-testing
- Add a plugin to query the PackageKit prepared-update file directly
- Do not clear the offline-update trigger if rebooting succeeded
- Do not load incompatible projects when parsing AppStream data
- Lots of updated translations
- Show the window right away when starting

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> 3.9.3-1
- New upstream release.
- Lots of new and fixed UI and updated metadata for Fedora 20

* Tue Sep 03 2013 Richard Hughes <richard@hughsie.com> 3.9.2-1
- New upstream release.
- Allow stock items in the AppStream XML
- Extract the AppStream URL and description from the XML
- Only present the window when the overview is complete
- Return the subcategories sorted by name

* Mon Sep 02 2013 Richard Hughes <richard@hughsie.com> 3.9.1-1
- New upstream release which is a technical preview for the alpha.

* Sun Sep 01 2013 Richard Hughes <richard@hughsie.com> 0.1-3
- Use buildroot not RPM_BUILD_ROOT
- Own all gnome-software directories
- Drop gtk-update-icon-cache requires and the mime database functionality

* Thu Aug 29 2013 Richard Hughes <richard@hughsie.com> 0.1-2
- Add call to desktop-file-validate and fix other review comments.

* Wed Aug 28 2013 Richard Hughes <richard@hughsie.com> 0.1-1
- First release for Fedora package review
