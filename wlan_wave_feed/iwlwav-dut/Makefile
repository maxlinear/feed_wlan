#
# Openwrt Makefile for dut tool
#
#
#

#### Includes ###################################
include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=iwlwav_dut
PKG_REV:=2d6b8fda375b85b1bbf9e5fd738147e5e3822a63
PKG_VERSION:=1.0
PKG_RELEASE:=1
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_PROJECT:=maxlinear
PKG_SOURCE_NAME:=dut.git
CONFIG_UGW_PKG_SOURCE_URL:=ssh://git@github.com
PKG_SOURCE_URL:=$(CONFIG_UGW_PKG_SOURCE_URL)/$(PKG_PROJECT)/$(PKG_SOURCE_NAME)
PKG_SOURCE_VERSION:=r1044+a+57
PKG_SOURCE_PROTO:=git
PKG_MIRROR_HASH:=fb7c488630adbbf13136a73bff24f10c37c59a36b320e12baa41219a5f020b28

PKG_MAINTAINER:=MaxLinear
PKG_LICENSE:=MaxLinear
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/iwlwav_dut-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk
-include $(INCLUDE_DIR)/package-version-override.mk

define Package/iwlwav_dut
	SECTION:=utils
	CATEGORY:=MaxLinear
	TITLE:=dut cli tool
	URL:=https://www.maxlinear.com
	DEPENDS:=+iwlwav_shared_header +libstdcpp
	MENU:=1
	VARIANT:=release
endef

define Package/iwlwav_dut/description
	Maxlinear DUT mode cli tool
endef

define Build/Prepare
	$(call Build/Prepare/Default)
	# Additional preparation steps
endef


CMAKE_SOURCE_DIR:=
CMAKE_OPTIONS+= \
	-DTARGET_PLATFORM=openwrt \
	-DCMAKE_INSTALL_PREFIX=/opt/intel \
	-DPLATFORM_BUILD_DIR=$(BUILD_DIR) \
	-DPLATFORM_STAGING_DIR=$(STAGING_DIR) \
	-DPLATFORM_INCLUDE_DIR=$(STAGING_DIR)/usr/include \
	-DMSGLIB=None \
	-DREVISION=$(PKG_SOURCE_VERSION) \
	-DPLATFORM_LIB_DIRECTORY=$(STAGING_DIR_HOSTPKG)/lib \
	-DTOOLCHAIN_DIR=$(TOOLCHAIN_DIR)	\
	-DSHARED_HEADERS_DIR=$(BUILD_DIR)/iwlwav_shared_header-$(PKG_VERSION)

define Build/Configure
	cmake -S $(PKG_BUILD_DIR) -B $(PKG_BUILD_DIR) $(CMAKE_OPTIONS)
endef

define Build/Compile
	cmake --build $(PKG_BUILD_DIR)/
endef

define Package/iwlwav_dut/install
	$(INSTALL_DIR) $(1)/opt/intel/wave/scripts/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/dut_cli/dut_cli $(1)/opt/intel/wave/scripts/
endef

$(eval $(call BuildPackage,iwlwav_dut))
