/**
 * @file trees.h
 * @author Sylvan Brocard (sbrocard@upmem.com)
 * @brief Header file for the trees project
 *
 */

#ifndef _H_TREES
#define _H_TREES /**< header guard */

#include <dpu.h>
#include <dpu_target.h>
#include <math.h>
typedef struct dpu_set_t dpu_set;

// Parameters holding struct
typedef struct Params {
    uint64_t npoints;
    uint64_t npadded;
    uint64_t npointperdpu;
    int nfeatures;
    float scale_factor;
    float threshold;
    float *mean;
    int isOutput;
    int nloops;
    int max_iter;
    uint32_t ndpu;
    dpu_set allset;
    int from_file;
    int verbose;
    float *features_mins;
    float *features_maxes;
} Params;

/**
 * @brief Data to track sample split
 *
 */
typedef struct SplitRecord {
    size_t feature; /**< Which feature to split on. */
    size_t pos; /**< Split samples array at the given position, i.e. count of
                   samples below threshold for feature. pos is >= end if the
                   node is a leaf. */
    double threshold;      /**< Threshold to split at. */
    double improvement;    /**< Impurity improvement given parent node. */
    double impurity_left;  /**< Impurity of the left split. */
    double impurity_right; /**< Impurity of the right split. */
} SplitRecord;

typedef struct Splitter {
    size_t* samples;
    size_t start;
    size_t end;

    size_t* features;
    size_t* constant_features;
    size_t n_features;

    double_t* Xf;
    size_t max_features;
    size_t min_samples_leaf;

} Splitter;

// /**
//  * @brief Node structure.
//  * Base storage structure for the nodes in a Tree object
//  */
// typedef struct Node {
//     size_t left_child;     /**< id of the left child of the node */
//     size_t right_child;    /**< id of the right child of the node  */
//     size_t feature;        /**< Feature used for splitting the node   */
//     double_t threshold;    /**< Threshold value at the node */
//     double_t impurity;     /**< Impurity of the node (i.e., the value of the
//                               criterion)  */
//     size_t n_node_samples; /**< Number of samples at the node  */
// } Node;

// /**
//  * @brief Tree structure.
//  * The Tree object is a binary tree structure constructed by the TreeBuilder.
//  * The tree structure is used for predictions and feature importances
//  */
// typedef struct Tree {
//     /* Input/Output layout */
//     size_t nfeatures;     /**< number of features in X */
//     size_t *n_classes;    /**< Number of classes in y[:, k] */
//     size_t n_outputs;     /**< Number of outputs in y */
//     size_t max_n_classes; /**< max(n_classes) */

//     /* Inner structures: values are stored separately from node structure,
//     since
//      * size is determined at runtime. */
//     size_t max_depth;    /**< Max depth of the tree */
//     size_t node_count;   /**< Counter for node IDs */
//     size_t capacity;     /**< Capacity of tree, in terms of nodes */
//     Node *nodes;         /**< Array of nodes */
//     double *value;       /**< [capacity, n_outputs, max_n_classes]
//                               array of values */
//     size_t value_stride; /**< = n_outputs * max_n_classes */

// } Tree;

// Function declarations
/** @name dpu_management.c */
/**@{*/
void allocate(Params *p);
void free_dpus(Params *p);
void load_kernel(Params *p, const char *DPU_BINARY);
void populateDpu(Params *p, float **features);
/**@}*/

/** @name input.c */
/**@{*/
void read_bin_input_with_int_targets(Params *p, const char *filename,
                                     float ***features_out, int **targets_out);
void read_txt_input_with_int_target(Params *p, const char *filename,
                                    float ***features_out, int **targets_out);
void save_dat_file_with_int_target(Params *p, const char *filename_in,
                                   float **features, int *targets);
void format_array_input(Params *p, float *data, float ***features_out);
/**@}*/
#endif
